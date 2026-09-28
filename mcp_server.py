import sys
import json
from client import RaftSnapshotManager

rsm = RaftSnapshotManager()

def handle_request(req):
    method = req.get("method")
    params = req.get("params", {})
    req_id = req.get("id")

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "raft_snapshot_op",
                        "description": "Take snapshot or install snapshot in Raft log manager",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "action": {"type": "string", "enum": ["take", "install"]},
                                "index": {"type": "integer"},
                                "term": {"type": "integer"},
                                "state": {"type": "object"}
                            },
                            "required": ["action", "index", "state"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {})
        if name == "raft_snapshot_op":
            act = args["action"]
            idx = args["index"]
            st = args["state"]
            if act == "take":
                ok = rsm.take_snapshot(idx, st)
                return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps({"success": ok, "remaining_log_len": len(rsm.log)})}]}}
            elif act == "install":
                rsm.install_snapshot(idx, args.get("term", 1), st)
                return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps({"installed": True, "last_index": idx})}]}}
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    for line in sys.stdin:
        if line.strip():
            req = json.loads(line)
            res = handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
