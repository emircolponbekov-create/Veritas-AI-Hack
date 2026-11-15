# Submission code walkthrough

No existing production code was changed during this completion pass. The only new delivered executable code is the six review cells of RESULTS_REVIEW.ipynb. The tables below explain each physical line. Blank lines have no action. All original MODEL/UI code and the legacy training notebook are preserved.

The local review branch was executed end-to-end. The Colab upload/extraction branch was syntax-checked and its path conditions were inspected; it was not executed in Colab. Its archive paths are also checked independently during release packaging. Visible outputs are artifact-review outputs, not training outputs.

## Review code cell 1

| Line | Code | What it does and why |
| --- | --- | --- |
| 1 | <code>from pathlib import Path</code> | Use filesystem paths consistently across Windows and Colab. |
| 2 | <code>import sys</code> | Allow importing the existing project modules after locating the release. |
| 3 | <code>import json</code> | Provide JSON support for the review environment; it does not fit or modify a model. |
| 4 | <code>import hashlib</code> | Compute a final SHA-256 check of the registry bytes. |
| 5 | <code>from collections import Counter</code> | Count the actual registry data states without guessing readiness. |
| 6 | <code>import pandas as pd</code> | Build the comparison table from independently checked per-system results. |
| 7 | <code>import matplotlib.pyplot as plt</code> | Plot saved estimates and measurements; no predictions are generated here. |

## Review code cell 2

| Line | Code | What it does and why |
| --- | --- | --- |
| 1 | <code>candidates = [Path.cwd(), *Path.cwd().parents]</code> | Search the current directory and its parents for the existing project, avoiding hardcoded Windows paths. |
| 2 | <code>ROOT = next((p for p in candidates if (p / "data/model_artifacts/multistation/registry.json").is_file()), None)</code> | Select a directory only if it contains the actual registry. |
| 3 | <code>if ROOT is None:</code> | Use the upload route only when the release is not already available locally. |
| 4 | <code>    from google.colab import files</code> | Open the standard one-time Colab upload chooser; local review never executes this branch. |
| 5 | <code>    from zipfile import ZipFile</code> | Read the supplied release ZIP instead of fetching hidden remote inputs. |
| 6 | <code>    from io import BytesIO</code> | Wrap uploaded ZIP bytes as a readable in-memory stream. |
| 7 | <code>    import stat</code> | Identify archive symbolic-link entries so they can be rejected. |
| 8 | <code>    uploaded = files.upload()</code> | Ask for the one release ZIP; uploading a CSV alone is insufficient for the multi-system review. |

| Line | Code | What it does and why |
| --- | --- | --- |
| 9 | <code>    if len(uploaded) != 1:</code> | Reject ambiguous uploads instead of guessing which bundle to use. |
| 10 | <code>        raise ValueError("Upload exactly one nuclear-water-release.zip")</code> | Explain how to resolve an incorrect upload count. |
| 11 | <code>    ROOT = Path("nuclear-water-release").resolve()</code> | Create a fixed, separate runtime destination under the current Colab directory. |
| 12 | <code>    ROOT.mkdir(exist_ok=False)</code> | Require a new extraction directory so existing runtime work cannot be overwritten. |
| 13 | <code>    with ZipFile(BytesIO(next(iter(uploaded.values())))) as archive:</code> | Inspect the uploaded archive before extracting any of its contents. |
| 14 | <code>        destinations = []</code> | Collect resolved targets to detect duplicate archive paths. |
| 15 | <code>        for item in archive.infolist():</code> | Check every ZIP member, including directory entries. |
| 16 | <code>            target = (ROOT / item.filename).resolve()</code> | Resolve each member against the intended extraction root. |

| Line | Code | What it does and why |
| --- | --- | --- |
| 17 | <code>            if not target.is_relative_to(ROOT) or "\\" in item.filename or ":" in item.filename or stat.S_ISLNK(item.external_attr &gt;&gt; 16):</code> | Reject paths outside the root, Windows drive/backslash paths and symbolic links. |
| 18 | <code>                raise ValueError("Unsafe release archive path")</code> | Stop extraction with a concrete reason before any unsafe path is written. |
| 19 | <code>            if target in destinations:</code> | Detect two members targeting the same path. |
| 20 | <code>                raise ValueError("Duplicate release archive path")</code> | Stop duplicate-path extraction, preserving a unique file-to-path mapping. |
| 21 | <code>            destinations.append(target)</code> | Record the safe destination before inspecting the next member. |
| 22 | <code>        archive.extractall(ROOT)</code> | Extract only after every member passed the path checks. This writes runtime inputs, never the original project bundle. |
| 23 | <code>print("Input bundle located. Original inputs and model artifacts will only be read.")</code> | State the read-only scope of the subsequent artifact checks. |

## Review code cell 3

| Line | Code | What it does and why |
| --- | --- | --- |
| 1 | <code>sys.path.insert(0, str(ROOT / "src/ui"))</code> | Make the existing UI loader importable from the selected release root. |
| 2 | <code>from multistation_loader import registry_snapshot, measurements_snapshot, verified_results</code> | Reuse the existing registry snapshot, MODEL adapter and independent export verifier; do not duplicate Parquet preparation. |
| 3 | <code>registry, token = registry_snapshot(ROOT)</code> | Read one validated registry version and retain its content hash for consistency checks. |
| 4 | <code>entries = registry["datasets"]</code> | Take per-system entries from the actual registry. |
| 5 | <code>print("Registry systems:", len(entries), "&#124; EIA plant IDs:", len({e["plant_id_eia"] for e in entries}))</code> | Report systems separately from unique EIA plant IDs. |
| 6 | <code>print("Data states:", dict(Counter(e["status"] for e in entries)))</code> | Print actual readiness categories, not an assumed list of trained models. |
| 7 | <code>print("No training: existing MODEL adapter and read-only export verifier only.")</code> | Label the provenance of the computation explicitly. |

## Review code cell 4

| Line | Code | What it does and why |
| --- | --- | --- |
| 1 | <code>rows = []</code> | Create a new in-memory review table, not a replacement source CSV. |
| 2 | <code>checked = {}</code> | Keep each validated export under its exact plant/system pair for the later example. |
| 3 | <code>for entry in entries:</code> | Verify each registry entry independently. |
| 4 | <code>    if entry["status"] != "ready_for_model_check" or entry["model_status"] not in {"existing_verified", "evaluated_verified"}:</code> | Only admit data cleared for model checking and a verified saved-model status. |
| 5 | <code>        continue</code> | Skip restricted/untrained systems without inventing a result. |
| 6 | <code>    measurements, audit = measurements_snapshot(entry, token, ROOT)</code> | Load that exact system through the existing adapter with source/eligibility/unit checks. |
| 7 | <code>    results, scores = verified_results(entry, measurements, token, ROOT)</code> | Verify the complete saved export and independently recompute its three MAEs. |
| 8 | <code>    beats = scores["model_delta_t_c"] &lt; min(scores["median_baseline_delta_t_c"], scores["seasonal_baseline_delta_t_c"])</code> | Compare Ridge with the lower of the two baselines for that system only. |

| Line | Code | What it does and why |
| --- | --- | --- |
| 9 | <code>    rows.append({"dataset_id": entry["dataset_id"], "Plant": entry["plant_name"], "System": entry["cooling_id_eia"], "Train": entry["split_counts"]["train"], "Validation": entry["split_counts"]["validation"], "Test": len(results), "Ridge MAE (C)": scores["model_delta_t_c"], "Overall median MAE (C)": scores["median_baseline_delta_t_c"], "Seasonal median MAE (C)": scores["seasonal_baseline_delta_t_c"], "Beats best baseline": beats})</code> | Record identity, all three split sizes and all three scores; weak results remain in the table. |
| 10 | <code>    checked[(entry["plant_id_eia"], entry["cooling_id_eia"])] = results</code> | Keep results tied to a compound identity so another system cannot supply the example. |
| 11 | <code>summary = pd.DataFrame(rows)</code> | Convert the verified row records into the visible comparison table. |
| 12 | <code>assert len(summary) == 17 and int(summary["Beats best baseline"].sum()) == 4, "Release results differ; investigate before submitting"</code> | Require the release expectation (17 evaluated, 4 better) to match observed artifacts; it never changes the data to force a match. |
| 13 | <code>display(summary)</code> | Save the full, honest table as a visible notebook output. |
| 14 | <code>print("17 systems evaluated; Ridge improves on the best baseline in 4, and is worse in 13. No models were reselected.")</code> | Explain the positive and negative results; no model is reselected. |

## Review code cell 5

| Line | Code | What it does and why |
| --- | --- | --- |
| 1 | <code>surry = checked[(3806, "CW1")]</code> | Select only the already checked Surry CW1 export. |
| 2 | <code>example = surry.loc[["2025-12"], ["reported_delta_t_c", "model_delta_t_c"]].copy()</code> | Select the actual December 2025 measured target and saved estimate by month. |
| 3 | <code>example["absolute_error_c"] = (example.model_delta_t_c - example.reported_delta_t_c).abs()</code> | Compute the absolute error from those two real values. |
| 4 | <code>display(example)</code> | Make the real failure example visible to judges. |
| 5 | <code>figure, axes = plt.subplots(figsize=(10, 4))</code> | Create a figure for the previously saved predictions; no training or inference is involved. |
| 6 | <code>plot = surry[["reported_delta_t_c", "median_baseline_delta_t_c", "seasonal_baseline_delta_t_c", "model_delta_t_c"]].copy()</code> | Use the measured target and all three saved estimates on the same test rows. |
| 7 | <code>plot.index = pd.to_datetime(plot.index)</code> | Turn YYYY-MM labels into a chronological datetime index. |
| 8 | <code>plot = plot.reindex(pd.date_range(plot.index.min(), plot.index.max(), freq="MS"))</code> | Insert empty calendar gaps rather than connecting excluded months as if they were observations. |

| Line | Code | What it does and why |
| --- | --- | --- |
| 9 | <code>plot.plot(ax=axes, marker=".")</code> | Draw the four series without changing their values. |
| 10 | <code>axes.set(xlabel="Held-out reporting month", ylabel="Cooling-system delta T (C)", title="Surry CW1: measured vs saved estimates; gaps are excluded months")</code> | Label the units, held-out period and gap meaning to prevent overinterpretation. |
| 11 | <code>figure.tight_layout()</code> | Keep labels inside the saved figure. |
| 12 | <code>display(figure)</code> | Embed the actual locally rendered plot in notebook outputs. |
| 13 | <code>plt.close(figure)</code> | Release the figure resource after capturing its output. |
| 14 | <code>print("2025-12 is a real error example, not evidence about ecosystem harm or safety.")</code> | Warn that the error is not a diagnosis of ecosystem harm or safety. |

## Review code cell 6

| Line | Code | What it does and why |
| --- | --- | --- |
| 1 | <code>assert hashlib.sha256((ROOT / "data/model_artifacts/multistation/registry.json").read_bytes()).hexdigest() == token</code> | Confirm that registry bytes remained equal to the initial snapshot hash. |
| 2 | <code>print("Registry snapshot remained unchanged. Review completed without training or overwriting MODEL files.")</code> | State exactly what was checked and that no MODEL file was overwritten. |
| 3 | <code>print("Original model choices: fixed Ridge alpha grid 0.1, 1, 10, 100; train 2010–2021; validation 2022–2023; test 2024–2025.")</code> | Describe the saved training protocol without claiming this notebook trained it. |
| 4 | <code>print("Features: same-month intake temperature and calendar sine/cosine. Discharge and current target are excluded from predictors.")</code> | List the permitted feature inputs and excluded target-leaking quantities. |

## Preserved code and test boundary

No function in the existing loaders, Ridge pipeline, Streamlit UI or tests was edited. The original Surry training notebook has 10 matching function definitions but no outputs; running it would train and export into data/, so it was not executed. Twenty existing appropriate tests were run successfully; a preparation-era test that invokes a writer was deliberately not included. Internal one-off documentation/packaging commands do not form part of the model or application.
