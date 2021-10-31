import os
from limber.operators.python_operator.operator import PythonOperator
from limber.imports.google import (
    CloudfunctionsFunction,
    StorageBucketObject,
    PubsubTopic,
)


class PythonOperatorGCP(PythonOperator):

    def get_terraform_json(self, *, stack, folder, cloud_storage_bucket):

        hash = self._write_cloud_function_code(folder=folder)

        source_dir = f"{self.dag.dag_id}/{self.task_id}"

        if len(self.upstream_tasks) > 0:
            trigger_resource = f"task_{self.dag.dag_id}_{self.upstream_tasks[0]}"
        else:
            trigger_resource = f"dag_{self.dag.dag_id}"

        PubsubTopic(
            stack,
            f"task_{self.dag.dag_id}_{self.task_id}",
            name=f"task_{self.dag.dag_id}_{self.task_id}",
        )

        storage_bucket_object = StorageBucketObject(
            stack,
            f"task_{self.task_id}",
            name=f"{source_dir}_{hash}.zip",
            bucket=cloud_storage_bucket.name,
            source=f"{source_dir}.zip",
        )

        CloudfunctionsFunction(
            stack,
            f"function_{self.task_id}",
            name=f"{self.dag.dag_id}-{self.task_id}",
            description=self.description,
            runtime="python37",
            available_memory_mb=self.memory,
            timeout=self.timeout,
            service_account_email=os.environ["CLOUD_FUNCTIONS_SERVICE_ACCOUNT_EMAIL"],
            source_archive_bucket=cloud_storage_bucket.name,
            source_archive_object=storage_bucket_object.name,
            event_trigger={
                "event_type": "providers/cloud.pubsub/eventTypes/topic.publish",
                "resource": trigger_resource
            },
            entry_point="cloudfunction_execution"
        )
