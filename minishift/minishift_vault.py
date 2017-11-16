import shutit 
import minishift

def setup():
	s1 = minishift.startup()
	s1.send('oc login -u system:admin')
	s1.send('rm -rf credscontroller')
	s1.send('git clone https://github.com/raffaelespazzoli/credscontroller')
	s1.send('cd credscontroller')
	s1.send('oc new-project vault-controller')
	s1.send('oc adm policy add-scc-to-user anyuid -z default')
	s1.send('oc create configmap vault-config --from-file=vault-config=./openshift/vault-config.json')
	s1.send('oc create -f ./openshift/vault.yaml')
	s1.send('oc create route passthrough vault --port=8200 --service=vault')
	s1.send(r"""export VAULT_ADDR=https://$(oc get route | grep -m1 vault | awk '{print $2}')""")
	s1.send('vault init -tls-skip-verify -key-shares=1 -key-threshold=1')
	s1.pause_point('https://blog.openshift.com/managing-secrets-openshift-vault-integration/ unseal vault')

if __name__ == '__main__':
	setup()
