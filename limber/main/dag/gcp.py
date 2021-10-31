from limber.main.dag.dag import DAG
from limber.imports.google import PubsubTopic, CloudSchedulerJob

class DAGGCP(DAG):

    def get_terraform_json(self, *, stack) -> {}:

        topic = PubsubTopic(
            stack,
            f"dag_{self.dag_id}",
            name=f"dag_{self.dag_id}"
        )

        CloudSchedulerJob(
            stack,
            f"job_{self.dag_id}",
            name=self.dag_id,
            description=self.description,
            schedule=self.schedule_interval,
            pubsub_target={
                "topic_name": topic.id,
                "data": "dGVzdA=="
            }
        )