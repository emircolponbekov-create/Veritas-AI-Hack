# Distribution verification — 15 November 2026

The correction starts from GitHub commit `82d89a491b619a6d49e1c296ee723ff37b619266`.
The original submitted data and evidence used byte-level SHA-256 manifests.
Git had normalized some CRLF text files to LF without changing those manifests,
causing valid inputs and reports to be rejected. Original bytes were restored
from the preserved local distribution, after checking that the differences were
only line endings. No model was trained, selected or tuned; no numeric source
value, result or scientific conclusion was changed. Existing integrity manifests
were preserved. `.gitattributes` disables further Git text conversion.

## Checks actually run on the corrected distribution

Using the existing Python environment with the pinned UI runtime dependencies:

| Check | Result |
| --- | --- |
| Source and reviewed-evidence integrity | 19 hashes matched across the 102-system registry and four review/publication manifests |
| Saved model comparisons | All 17 verified through the existing read-only loaders; Ridge better than the better median in 4, worse in 13 |
| Environmental report tests | 10 passed |
| Story-support tests | 11 passed |
| Scenario tests | 5 passed |
| UI integration tests | 28 passed; existing `VERITAS_UI_NO_SOCKET_TESTS=1` test-only workaround |
| Saved review notebook | 8 output objects retained, no saved error outputs |

Run the read-only distribution check from any working directory:

```sh
python submission/verify_distribution.py --results
```

Run the existing tests from the project root with the installed environment:

```sh
python -m unittest discover -s tests/model -p test_environment_report.py
python -m unittest discover -s tests/model -p test_site_support.py
python -m unittest discover -s tests/fuel
python -m unittest discover -s tests/ui
```

On Windows hosts where test-only socket initialization is restricted, set
`$env:VERITAS_UI_NO_SOCKET_TESTS='1'` in PowerShell before the UI command. This is
not a production app setting. Do not run broad model-test discovery as a release
check: it includes development training/writer tests.

## Limits

These checks used an existing environment, not a fresh dependency installation.
The notebook's prior visible outputs were preserved; the plotting notebook was
not rerun in this pass. Separate training/development tests requiring matplotlib
and scikit-learn were not run. The normal local server/browser attempt could not
be confirmed, so this record does not certify desktop, mobile, CSS or JavaScript
rendering. AppTest is not a substitute for visual inspection. The team should
rehearse the normal app before recording its demo.

Passing checks do not establish ecological safety, source authenticity, expert
review, or compliance with the competition's team and weekend-work rules.
Participant details and the official submission receipt are team actions.
