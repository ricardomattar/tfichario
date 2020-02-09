import post
import glb

glb.username='admin'
glb.password='skandar'

pesquisa = post.call(method='hospedes.rpc_query', query='ricardo%')
print(pesquisa)