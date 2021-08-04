from .errors import ImplementaionError, DuplicateMetric
from functools import wraps 


class MetricMeta(type):
    """Meta class for all the Metric defined,Need to run clear_base_instance before customising the base class"""

    __base_formed = False
    __base_instance =  None
    def __new__(cls,name,base,dic):
        if len(base) > 0 and  cls.__base_formed:
            if cls.__base_instance is base[0]:
                if "__init__" in dic or "__new__" in dic or "__slots__" in dic:
                    raise ImplementaionError(f"{name} is not instantiable if it inherits {cls.__base_instance} nor it can use slots")

            else:
                msg = "Base class or your own custome base class should be inherited first "
                raise ImplementaionError(msg)
            return super().__new__(cls,name,base,dic)
        else:
            cls.__base_formed =  True
            cls.__base_instance = super().__new__(cls,name,base,dic)
            # print(cls.__base_instance)

            return cls.__base_instance


    @classmethod
    def clear_base_instance(cls):
        cls.__base_instance = None
        cls.__base_formed = False


class Base(metaclass=MetricMeta):
    __metric_pool = {}

    def __init__(self,registry=None):
        print(self.__metric_pool)
        self.__collection_registry = registry
        for metric_name,metric_value in self.__metric_pool.items():
            self.__metric_pool[metric_name] = metric_value(self)
        print("dasdadada",self.__metric_pool)
        
            

    @property
    def get_collection_registry(self):
        return self.__collection_registry
    
    @property
    def get_defined_metrics(self)-> dict:
        return self.__metric_pool


    @classmethod
    def set_metric(cls,f):
        if not f.__name__ in cls.__metric_pool:
            cls.__metric_pool[f.__name__] = f
        else:
            # print(cls.__metric_pool,f.__name__)
            raise DuplicateMetric(f.__name__)
        @wraps(f)
        def inner(*args,**kw):
            return f(*args,**kw)
        return inner
