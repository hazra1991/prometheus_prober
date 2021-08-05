import requests
from .probe_scheduler import BaseProber



class Prober(BaseProber):
 
    def __init__(self,name , interval , metric):
        print(metric)
        metric = metric.get_defined_metrics
        self.counter = metric["counter"]
        super().__init__(name,interval)


    # pylint: disable=broad-except
    def probe(self):
        print("runnint")

        res  = requests.get("http://127.0.0.1:5000/upload")
        if res.status_code == 200:
            print("this is started ")
            # logger()
            self.counter.labels("succeeded").inc()
        else:
            self.counter.labels("Failed").inc()


class Prober(BaseProber):
 
    def __init__(self,name , interval , metric):
        print(metric)
        metric = metric.get_defined_metrics
        self.counter = metric["counter"]
        super().__init__(name,interval)


    # pylint: disable=broad-except
    def probe(self):
        print("runnint")

        res  = requests.post("http://127.0.0.1:5000/upload")
        if res.status_code == 200:
            print("this is started ")
            # logger()
            self.counter.labels("succe").inc()
        else:
            self.counter.labels("Fai").inc()

        