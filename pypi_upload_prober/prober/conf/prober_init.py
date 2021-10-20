from . import env
from ..src.prober_def import AvailabilityProber
from ..src.metric import Metrics
from prometheus_client import CollectorRegistry, Info


#####################################
# Define the collection registries ##
#####################################

Availability_collection = CollectorRegistry(auto_describe=True)

##########################################
# Set meta INFO on Collection registries #
##########################################

doc = 'Collection metric endpoint for PYPI uploader service'
Info(name="PYPI_upload_service", documentation=doc, registry=Availability_collection).info({
        'source': __file__,
        'version': env.__version__
    })


#####################################
# Create  probers to be scheduled  ##
#####################################

# Create all the probers inside the PROBER_LIST

PROBER_LIST = [

        AvailabilityProber(
            name="Availability_prober",
            metric=Metrics(Availability_collection),
            interval=300,
            log_dir=env.log_dir
            
        )

]
