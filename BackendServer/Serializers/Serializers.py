from termcolor import colored
from datetime import datetime
class Serializer() :


        @staticmethod
        def Serializer(object : object, fields : list ) :
                
                object_data : dict = object.__dict__
                data : dict = {}

                if(fields) :
                       
                        for field in fields :
                               

                              data[field] = object_data[field]
                        
                              if( isinstance(data[field], datetime) ) :
                                    
                                    data[field] = data[field].timestamp()

                        return data 
                
                else :
                       
                      raise Exception("The feilds parameter required on serializer")
                               

        def ListSerializer(objects : list[object], fields : list ) :
               
               data = []
               try :

                for object in objects :
                                         
                     data.append(Serializer.Serializer(object=object, fields=fields))

                return data
               
               except Exception as e :
                     
                     print( colored(f"Error : {e}", "red", attrs=["bold"]))
