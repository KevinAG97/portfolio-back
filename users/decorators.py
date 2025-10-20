from functools import wraps
from drf_yasg.utils import swagger_auto_schema

def tag_all_views(tag):
    # Adiciona automaticamente a tag baseada no nome da classe
    def decorator(view_class):
        action_methods = {
            'list':None,
            'create':None,
            'retrieve':None,
            'partial_update':None,
            'destroy':None,
        }
        desc_methods =  {
            'list': f'Lista todas as {tag}',
            'create':f'Cria uma {tag}',
            'retrieve':f'Retorna uma {tag} específica',
            'partial_update':f'Atualiza campos específicos de uma {tag}',
            'update':f'Atualiza todos os campos de uma {tag}',
            'destroy': f'Exclui uma {tag} específica',
        }

        for method_name in action_methods:
            if hasattr(view_class, method_name):
                action_methods[method_name] = getattr(view_class, method_name)
                desc = desc_methods[method_name]
                
                @swagger_auto_schema(tags=[tag], operation_description=desc)
                @wraps(action_methods[method_name])   
                def method(self, request, *args, **kwargs):
                    original_method = action_methods[self.action]
                    return original_method(self, request, *args, **kwargs)

                setattr(view_class, method_name, method)

        if hasattr(view_class, 'update'):
            update_method = getattr(view_class, 'update')       
            @swagger_auto_schema(tags=[tag], operation_description=desc_methods['update'])
            @wraps(update_method)
            def method_update(self, request, *args, **kwargs):
                return update_method(self, request, *args, **kwargs)
            setattr(view_class, 'update', method_update)
            
        return view_class
    return decorator