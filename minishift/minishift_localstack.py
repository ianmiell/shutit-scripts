import shutit 
import minishift

def setup():
	s1 = minishift.startup()
	s1.send('oc login -u system:admin')
	s1.send('oc project myproject')
	s1.send_file('/tmp/new_scc.yaml','''allowHostDirVolumePlugin: false
allowHostIPC: false
allowHostNetwork: false
allowHostPID: false
allowHostPorts: false
allowPrivilegedContainer: false
allowedCapabilities: null
apiVersion: v1
defaultAddCapabilities: null
fsGroup:
  type: MustRunAs
groups:
- system:authenticated
kind: SecurityContextConstraints
metadata:
  annotations:
    kubernetes.io/description: restricted denies access to all host features and requires
      pods to be run with a UID, and SELinux context that are allocated to the namespace.  This
      is the most restrictive SCC.
  name: restricted
  selfLink: /api/v1/securitycontextconstraintsrestricted
priority: null
readOnlyRootFilesystem: false
requiredDropCapabilities:
- KILL
- MKNOD
- SYS_CHROOT
runAsUser:
  type: RunAsAny
seLinuxContext:
  type: MustRunAs
supplementalGroups:
  type: RunAsAny
volumes:
- configMap
- downwardAPI
- emptyDir
- persistentVolumeClaim
- secret''')
	s1.send('oc update -f /tmp/new_scc.yaml')
	s1.send('oc login -u developer -p developer')
	s1.send('oc delete all --all')
	s1.send('''oc new-app -e DEBUG=1 localstack/localstack --name="localstack"''')
	host = s1.send_and_get_output(r"""minishift console --machine-readable | grep HOST | sed 's/^HOST=\(.*\)/\1/'""")
	s1.send('oc delete routes --all')
	s1.send_file('/tmp/routes.yaml','''apiVersion: v1
kind: Route
metadata:
  name: apigateway
spec:
  host: apigateway-test.''' + host + '''.nip.io
  port:
    targetPort: 4567-tcp
  to:
    kind: Service
    name: localstack''')
	s1.send('oc create -f /tmp/routes.yaml')

	s1.send_file('/tmp/routes.yaml','''apiVersion: v1
kind: Route
metadata:
  name: cloudformation
spec:
  host: cloudformation-test.''' + host + '''.nip.io
  port:
    targetPort: 4581-tcp
  to:
    kind: Service
    name: localstack''')
	s1.send('oc create -f /tmp/routes.yaml')

	s1.send_file('/tmp/routes.yaml','''apiVersion: v1
kind: Route
metadata:
  name: cloudwatch
spec:
  host: cloudwatch-test.''' + host + '''.nip.io
  port:
    targetPort: 4582-tcp
  to:
    kind: Service
    name: localstack''')
	s1.send('oc create -f /tmp/routes.yaml')

	s1.send_file('/tmp/routes.yaml','''apiVersion: v1
kind: Route
metadata:
  name: dynamodb
spec:
  host: dynamodb-test.''' + host + '''.nip.io
  port:
    targetPort: 4569-tcp
  to:
    kind: Service
    name: localstack''')
	s1.send('oc create -f /tmp/routes.yaml')

	s1.send_file('/tmp/routes.yaml','''apiVersion: v1
kind: Route
metadata:
  name: dynamodbstreams
spec:
  host: dynamodbstreams-test.''' + host + '''.nip.io
  port:
    targetPort: 4570-tcp
  to:
    kind: Service
    name: localstack''')
	s1.send('oc create -f /tmp/routes.yaml')

	s1.send_file('/tmp/routes.yaml','''apiVersion: v1
kind: Route
metadata:
  name: es
spec:
  host: es-test.''' + host + '''.nip.io
  port:
    targetPort: 4578-tcp
  to:
    kind: Service
    name: localstack''')
	s1.send('oc create -f /tmp/routes.yaml')

	s1.send_file('/tmp/routes.yaml','''apiVersion: v1
kind: Route
metadata:
  name: firehose
spec:
  host: firehose-test.''' + host + '''.nip.io
  port:
    targetPort: 4573-tcp
  to:
    kind: Service
    name: localstack''')
	s1.send('oc create -f /tmp/routes.yaml')

	s1.send_file('/tmp/routes.yaml','''apiVersion: v1
kind: Route
metadata:
  name: kinesis
spec:
  host: kinesis-test.''' + host + '''.nip.io
  port:
    targetPort: 4568-tcp
  to:
    kind: Service
    name: localstack''')
	s1.send('oc create -f /tmp/routes.yaml')

	s1.send_file('/tmp/routes.yaml','''apiVersion: v1
kind: Route
metadata:
  name: lambda
spec:
  host: lambda-test.''' + host + '''.nip.io
  port:
    targetPort: 4574-tcp
  to:
    kind: Service
    name: localstack''')
	s1.send('oc create -f /tmp/routes.yaml')

	s1.send_file('/tmp/routes.yaml','''apiVersion: v1
kind: Route
metadata:
  name: redshift
spec:
  host: redshift-test.''' + host + '''.nip.io
  port:
    targetPort: 4577-tcp
  to:
    kind: Service
    name: localstack''')
	s1.send('oc create -f /tmp/routes.yaml')

	s1.send_file('/tmp/routes.yaml','''apiVersion: v1
kind: Route
metadata:
  name: route53
spec:
  host: route53-test.''' + host + '''.nip.io
  port:
    targetPort: 4580-tcp
  to:
    kind: Service
    name: localstack''')
	s1.send('oc create -f /tmp/routes.yaml')

	s1.send_file('/tmp/routes.yaml','''apiVersion: v1
kind: Route
metadata:
  name: s3
spec:
  host: s3-test.''' + host + '''.nip.io
  port:
    targetPort: 4572-tcp
  to:
    kind: Service
    name: localstack''')
	s1.send('oc create -f /tmp/routes.yaml')

	s1.send_file('/tmp/routes.yaml','''apiVersion: v1
kind: Route
metadata:
  name: ses
spec:
  host: ses-test.''' + host + '''.nip.io
  port:
    targetPort: 4579-tcp
  to:
    kind: Service
    name: localstack''')
	s1.send('oc create -f /tmp/routes.yaml')

	s1.send_file('/tmp/routes.yaml','''apiVersion: v1
kind: Route
metadata:
  name: sns
spec:
  host: sns-test.''' + host + '''.nip.io
  port:
    targetPort: 4575-tcp
  to:
    kind: Service
    name: localstack''')
	s1.send('oc create -f /tmp/routes.yaml')

	s1.send_file('/tmp/routes.yaml','''apiVersion: v1
kind: Route
metadata:
  name: sqs
spec:
  host: sqs-test.''' + host + '''.nip.io
  port:
    targetPort: 4576-tcp
  to:
    kind: Service
    name: localstack''')
	s1.send('oc create -f /tmp/routes.yaml')

	s1.send_file('/tmp/routes.yaml','''apiVersion: v1
kind: Route
metadata: {}
apiVersion: v1
kind: Route
metadata:
  name: web
spec:
  host: web-test.''' + host + '''.nip.io
  port:
    targetPort: 8080-tcp
  to:
    kind: Service
    name: localstack''')
	s1.send('oc create -f /tmp/routes.yaml')
	s1.send_until('oc get pods | grep localstack | grep -v deploy | grep Running | wc -l','1')
	s1.send('minishift console')
	s1.multisend('aws configure',{'AWS Access Key':'any','AWS Secret':'any','Default region':'any','Default output':''})
	s1.send('''aws --endpoint-url=http://kinesis-test.''' + host + '''.nip.io kinesis list-streams''')
	s1.send('''aws --endpoint-url=http://kinesis-test.''' + host + '''.nip.io kinesis create-stream --stream-name teststream --shard-count 2''')
	s1.send('''aws --endpoint-url=http://kinesis-test.''' + host + '''.nip.io kinesis list-streams''')
	s1.interact()
	

if __name__ == '__main__':
	setup()
