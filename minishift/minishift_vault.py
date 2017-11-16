import shutit 
import minishift

# cf: https://blog.openshift.com/managing-secrets-openshift-vault-integration/
# cf: 

def setup():
	s1 = minishift.startup()
	s1.send('rm -rf credscontroller')
	s1.send('xz -d -c vault.xz > vault')
	s1.send('git clone https://github.com/ianmiell/credscontroller')
	s1.send('cd credscontroller')
	s1.send('oc delete project vault-controller || true')
	s1.send('while true; do oc new-project vault-controller && break; sleep 4; done')
	s1.send('oc adm policy add-scc-to-user anyuid -z default')
	s1.send('oc create configmap vault-config --from-file=vault-config=./openshift/vault-config.json')
	s1.send('oc create -f ./openshift/vault.yaml')
	s1.send('oc create route passthrough vault --port=8200 --service=vault')
	s1.send(r"""export VAULT_ADDR=https://$(oc get route | grep -m1 vault | awk '{print $2}')""")
	# TODO: wait
	output = s1.send_and_get_output('../vault init -tls-skip-verify -key-shares=1 -key-threshold=1')
	keysline = output.split('\n')[0]
	rootline = output.split('\n')[1]
	print keysline
	print rootline
	s1.pause_point('https://blog.openshift.com/managing-secrets-openshift-vault-integration/ unseal vault')

if __name__ == '__main__':
	setup()
