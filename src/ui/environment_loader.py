"""Read published evidence-report v1 without generating, fitting or caching."""
from dataclasses import dataclass
from datetime import date
import hashlib
import importlib
import json
import logging
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[2]
REPORTS = Path('data/environment_reports/v1')
LOGGER = logging.getLogger(__name__)
SECTION_IDS = ('water', 'animals_plants', 'people', 'climate', 'unknowns')
STATUSES = {'partial_evidence', 'insufficient_evidence', 'context_only'}


class ReviewRequired(ValueError):
    """A publication contains evidence that cannot be shown before review."""


@dataclass(frozen=True)
class ReportSnapshot:
    state: str
    report: dict | None = None
    technical: dict | None = None
    version: str | None = None


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def text(value):
    return isinstance(value, str) and bool(value.strip())


def validate_public(report, plant_id):
    """Check presentation fields that the publication reader does not inspect."""
    require(isinstance(report, dict), 'report_shape')
    require(type(report['plant_id_eia']) is int and report['plant_id_eia'] == plant_id, 'identity')
    require(type(report['report_version']) is int and report['report_version'] == 1, 'version')
    require(report['language'] == 'en', 'language')
    require(report['method'] == 'curated_evidence_rules_not_trained_safety_model', 'method')
    require(report['expert_review_status'] == 'not_performed', 'expert_review_status')
    require(report['status'] in STATUSES - {'context_only'}, 'report_status')
    for field in ('station_name', 'period_label', 'summary', 'as_of'):
        require(text(report[field]), 'missing_' + field)
    date.fromisoformat(report['as_of'])
    sections = report['sections']
    require(isinstance(sections, list), 'sections_shape')
    require([section['id'] for section in sections] == list(SECTION_IDS), 'section_order')
    for section in sections:
        require(text(section['title']) and section['status'] in STATUSES, 'section_header')
        require(isinstance(section['paragraphs'], list) and bool(section['paragraphs']), 'paragraphs_shape')
        require(all(text(p) for p in section['paragraphs']), 'paragraph_text')
        for field in ('claim_ids', 'references', 'periods', 'limitations'):
            require(isinstance(section[field], list), 'section_' + field)
        require(all(text(value) for value in section['claim_ids'] + section['limitations']), 'section_labels')
        for period in section['periods']:
            require(text(period['label']), 'period_label')
            for bound in ('start', 'end'):
                if period.get(bound) is not None:
                    date.fromisoformat(period[bound])
        for ref in section['references']:
            for field in ('source_id', 'claim_id', 'title', 'url', 'role', 'public_locator', 'locator', 'support_note'):
                require(text(ref[field]), 'reference_' + field)
            url = urlsplit(ref['url'])
            require(url.scheme in {'http', 'https'} and bool(url.netloc) and not url.username, 'source_url')
            require(ref['claim_id'] in section['claim_ids'], 'reference_claim')


def validate_scope(report, technical, plant_id):
    """Do not turn a site publication or disputed claim into a wider verdict."""
    require(isinstance(technical, dict), 'technical_shape')
    claims = technical['accepted_claims']
    require(isinstance(claims, list) and isinstance(technical['local_checks'], dict), 'ledger_shape')
    by_id = {}
    for claim in claims:
        require(claim['plant_id_eia'] == plant_id and type(claim['plant_id_eia']) is int, 'claim_identity')
        require(claim['id'] not in by_id and text(claim['geography']), 'claim_scope')
        require(claim['kind'] in {'observation', 'model_estimate', 'scenario', 'general_context'}, 'claim_kind')
        if claim['conflict_state'] == 'unresolved' or claim['review_status'] != 'reviewed_for_support':
            raise ReviewRequired('source_review')
        require(claim['conflict_state'] in {'none_identified', 'different_endpoint'}, 'conflict_state')
        by_id[claim['id']] = claim
    for section in report['sections']:
        for identifier in section['claim_ids']:
            require(identifier in by_id and by_id[identifier]['section'] == section['id'], 'claim_section')
        if section['status'] == 'context_only':
            require(all(by_id[c]['kind'] == 'general_context' for c in section['claim_ids']), 'context_scope')
    if report['status'] == 'insufficient_evidence':
        require(not claims and not any(s['references'] for s in report['sections']), 'insufficient_scope')
    water = technical['local_checks'].get('water')
    if water is not None:
        require(isinstance(water, dict) and text(water['system']), 'water_system_scope')


def report_snapshot(plant_id, root=ROOT):
    """Every call rereads the manifest and artifacts; no previous-site fallback."""
    stage = 'station_selection'
    try:
        require(type(plant_id) is int and plant_id > 0, 'plant_id')
        directory = Path(root).resolve() / REPORTS / f'eia_{plant_id}'
        require(directory.resolve().is_relative_to(Path(root).resolve()), 'publication_path')
        if not directory.exists():
            return ReportSnapshot('missing')
        for name in ('ready.json', 'report.en.json', 'report.en.md', 'technical.json'):
            require((directory / name).resolve().is_relative_to(directory.resolve()), 'artifact_path')
        stage = 'module_import'
        reader = importlib.import_module('src.model.environment_report').read_report
        stage = 'manifest'
        manifest_bytes = (directory / 'ready.json').read_bytes()
        manifest = json.loads(manifest_bytes)
        require(type(manifest['report_version']) is int and manifest['report_version'] == 1, 'manifest_version')
        stage = 'publication_reader'
        report = reader(directory, plant_id)
        technical = json.loads((directory / 'technical.json').read_bytes())
        stage = 'public_contract'
        validate_public(report, plant_id)
        stage = 'evidence_scope'
        validate_scope(report, technical, plant_id)
        stage = 'stable_publication'
        require((directory / 'ready.json').read_bytes() == manifest_bytes, 'publication_race')
        for name, expected in manifest['sha256'].items():
            require(hashlib.sha256((directory / name).read_bytes()).hexdigest() == expected, 'artifact_race')
        state = 'ready' if report['status'] == 'partial_evidence' else 'insufficient_evidence'
        return ReportSnapshot(state, report, technical, hashlib.sha256(manifest_bytes).hexdigest())
    except ImportError:
        state, reason = 'module_unavailable', 'import'
    except ReviewRequired:
        state, reason = 'review_required', 'source_review'
    except (OSError, ValueError, KeyError, TypeError, AttributeError, OverflowError):
        state, reason = 'evidence_unavailable', 'publication_validation'
    LOGGER.warning('Environmental report withheld: plant_id=%s state=%s reason=%s stage=%s', plant_id, state, reason, stage)
    return ReportSnapshot(state)
