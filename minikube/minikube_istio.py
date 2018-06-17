import shutit
import minikube

def istio_setup(s):
	# cf: https://istio.io/docs/guides/bookinfo.html
	#s.send('rm -rf istio-*')
	#s.send('curl -L https://git.io/getLatestIstio | sh -')
	#s.send('cd istio-*')
	#s.send('export PATH=$PWD/bin:$PATH')
	#s.send('kubectl delete -f install/kubernetes/istio-initializer.yaml || true')
	#s.send('kubectl apply -f install/kubernetes/istio-auth.yaml')
	#s.send('kubectl apply -f install/kubernetes/istio-initializer.yaml')
	#s.send_until('kubectl get pods -n istio-system --no-headers | wc -l','6')
	#s.send_until('kubectl get pods -n istio-system --no-headers | grep Running | wc -l','6')
	#s.send('kubectl apply -f samples/bookinfo/kube/bookinfo.yaml')
	#s.send("""export GATEWAY_URL=$(kubectl get po -n istio-system -l istio=ingress -n istio-system -o 'jsonpath={.items[0].status.hostIP}'):$(kubectl get svc istio-ingress -n istio-system -n istio-system -o 'jsonpath={.spec.ports[0].nodePort}')""")
	#s.send_until('curl -o /dev/null -s -w "%{http_code}\n" http://${GATEWAY_URL}/productpage','200')
	## You can now use this sample to experiment with Istio's features for traffic routing, fault injection, rate limitting, etc.. To proceed, refer to one or more of the Istio Guides, depending on your interest. Intelligent Routing is a good place to start for beginners.

	# Try again:
	# cf: https://github.com/controlplaneio/theseus/blob/2e5f0d8ea420958d7029414240deb4c01c65e4c3/local-istio.sh

	# preflight_checks:
	if s.send_and_get_output("""minikube status --format '{{.MinikubeStatus}}'""") != 'Running':
		s.send('minikube start')
	s.send('sleep 5')
	minikube_images = s.send_and_get_output('''minikube ssh docker images | tail -n +2''')
	print minikube_images
	s.pause_point('')
	# minikube-import
	

if __name__ == "__main__":
	s = minikube.startup(delete=True)
	istio_setup(s)

