from src.prober_def import AvailibilityProber
from src.metric import Metrics
from prometheus_client import CollectorRegistry,Info
import env

######################################
## Define the collection registries ##
######################################

Availibility_collection = CollectorRegistry(auto_describe=True)
# registry2 = CollectorRegistry(auto_describe=True)

##########################################
# Set meta INFO on Collection registries #
##########################################

doc = 'Collection metric endpoint for PYPI uploader service'
Info(name="PYPI_upload_service", documentation=doc, registry=Availibility_collection).info({
        'source': __file__,
        'version': env.prober_version
    })


######################################
## Create  probers to be scheduled  ## 
######################################

# Create all the probers inside the PROBER_LIST

PROBER_LIST = [

        AvailibilityProber(
            name = "Availibility_prober",
            interval = 6,
            metric=Metrics(Availibility_collection),
            
        )
]
