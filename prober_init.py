from src.prober_def import Prober
from src.metric import Metrics,Metrics2
from prometheus_client import CollectorRegistry,Info

######################################
## Define the collection registries ##
######################################

registry1 = CollectorRegistry(auto_describe=True)
registry2 = CollectorRegistry(auto_describe=True)

##########################################
# Set meta INFO on Collection registries #
##########################################
Info(name="dummy1", documentation='Provide if any', registry=registry1).info({
        'source': "filenname",
        'version': "__version__"
    })


######################################
## Create  probers to be scheduled  ## 
######################################

PROBER_LIST = (
    
        Prober(
            name = "prober1",
            interval = 3,
            metric=Metrics(registry1),
            
        ),
        Prober(
            name = "prober1",
            interval = 3,
            metric=Metrics2(registry2),
            
        )
    )
