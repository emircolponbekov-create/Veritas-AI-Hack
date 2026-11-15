"""Execute each notebook code cell sequentially, save actual outputs, no Jupyter server needed."""
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path
import base64
import io
import json
import traceback

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def run(path):
    notebook = json.loads(path.read_text(encoding="utf-8"))
    namespace = {"__name__": "__notebook__"}
    active_outputs = []

    def display(value):
        active_outputs.append({"output_type": "display_data", "metadata": {},
                               "data": {"text/plain": str(value)}})

    def show():
        for number in plt.get_fignums():
            buffer = io.BytesIO()
            plt.figure(number).savefig(buffer, format="png", dpi=140)
            active_outputs.append({"output_type": "display_data", "metadata": {},
                                   "data": {"image/png": base64.b64encode(buffer.getvalue()).decode("ascii")}})

    namespace["display"] = display
    plt.show = show
    count = 0
    for cell in notebook["cells"]:
        if cell["cell_type"] != "code":
            continue
        count += 1
        cell["execution_count"] = count
        active_outputs = []
        output = io.StringIO()
        try:
            with redirect_stdout(output), redirect_stderr(output):
                exec(compile("".join(cell["source"]), f"{path.name}:cell-{count}", "exec"), namespace)
        except Exception as error:
            active_outputs.append({"output_type": "error", "ename": type(error).__name__,
                                   "evalue": str(error), "traceback": traceback.format_exc().splitlines()})
            cell["outputs"] = active_outputs
            path.write_text(json.dumps(notebook, ensure_ascii=False, indent=1), encoding="utf-8")
            raise
        text = output.getvalue()
        cell["outputs"] = ([{"output_type": "stream", "name": "stdout", "text": text}] if text else []) + active_outputs
        print(f"Cell {count}: OK")
    notebook["metadata"]["execution_note"] = "Executed locally, sequential Python exec of every code cell with captured real outputs; Colab UI not executed."
    path.write_text(json.dumps(notebook, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"All {count} code cells completed; outputs saved in {path}")


if __name__ == "__main__":
    run(Path(__file__).with_name("surry_model.ipynb"))
