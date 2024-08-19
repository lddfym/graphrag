from graphrag.index.cli import (
    _get_progress_reporter,
    _create_default_config
)
from graphrag.index.config import PipelineConfig
from graphrag.index.progress import ProgressReporter
from graphrag.index.workflows import load_workflows
import json

root = "/Users/liudongdong04/work/github/graphrag/note/demo"
verbose = False
dryrun = False
reporter: ProgressReporter = _get_progress_reporter(None)
piplineConfig: PipelineConfig = _create_default_config(
    root, None, verbose, dryrun, reporter)
loaded_workflows = load_workflows(piplineConfig.workflows)


graph = []
for wk in loaded_workflows.workflows:
    wkname = wk.workflow.name
    graph.append({
        "workflow_name": wkname,
        "workflow": wk.workflow.export()
    })

graph_msg = json.dumps(graph, ensure_ascii=False, indent=2)
print(graph_msg)
with open('index_flow.json', 'w') as f:
    f.write(graph_msg)
