from .errors import ImplementaionError, DuplicateMetric
from functools import wraps
import inspect

# CAUTION DONOT ALTER THIS FILE !!!

class MetricMeta(type):
    """Meta class for all the Metric defined,Need to run clear_base_instance before customising the base class"""

    __base_formed = False
    __base_instance =  None
    def __new__(cls,name,base,dic):
        if len(base) > 0 and  cls.__base_formed:
            if cls.__base_instance is base[0]:
                if "__init__" in dic or "__new__" in dic or "__slots__" in dic:
                    raise ImplementaionError(f"{name} is not instantiable if it inherits {cls.__base_instance} nor it can use slots")
                for k,v in dic.items():
                    if inspect.isclass(v):
                        msg = f"Metric cannot have a direct class '{k}'. It can only have a function that resembles metric types"
                        raise ImplementaionError(msg)   
            else:
                msg = "Base class should be inherited first "
                raise ImplementaionError(msg)
            return super().__new__(cls,name,base,dic)
        else:
            cls.__base_formed =  True
            cls.__base_instance = super().__new__(cls,name,base,dic)
            return cls.__base_instance


    @classmethod
    def clear_base_instance(cls):
        cls.__base_instance = None
        cls.__base_formed = False


class Base(metaclass=MetricMeta):
    """base class for all the user defined matrics"""

    __metric_pool = {}

    def __init__(self,registry=None):
        cls_name =  self.__class__.__name__
        self.__collection_registry = registry
        self.__plugged_metrics = {}
        context = self.__metric_pool.get(cls_name)
        for metric_name,metric_value in context.items():
            self.__plugged_metrics[metric_name] = metric_value(self)

        
    @property
    def get_collection_registry(self):
        return self.__collection_registry
    
    @property
    def get_defined_metrics(self)-> dict:
        return self.__plugged_metrics

    @classmethod
    def clean(cls):
        # Cleans the memory for cached metrics
       cls.__metric_pool.clear()

    @classmethod
    def set_metric(cls,f):
        class_name = f.__qualname__[0:len(f.__qualname__) - (len(f.__name__) + 1)]
        print(class_name)
        if class_name in cls.__metric_pool:
            cls_context = cls.__metric_pool[class_name]
        else:
            cls.__metric_pool[class_name] = {}
            cls_context =  cls.__metric_pool[class_name]

        if not f.__name__ in cls_context:
            cls_context[f.__name__] = f
        else:
            raise DuplicateMetric(f.__name__)
        @wraps(f)
        def inner(*args,**kw):
            return f(*args,**kw)
        return inner
