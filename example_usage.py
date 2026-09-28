from client import RaftSnapshotManager

manager = RaftSnapshotManager()
manager.log = [(1, "x=1"), (1, "x=2"), (2, "x=3")]
manager.take_snapshot(up_to_index=2, state_dict={"x": 2})

print("Remaining log entries:", manager.log)
print("Snapshot state:", manager.snapshot_state)
print("Last included index:", manager.last_included_index)
