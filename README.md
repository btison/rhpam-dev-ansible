Ansible playbook for provisioning RHPAM (Business Central + KIE Server + Postgres)

Prerequisite: import image intp openshift namespace
```
$ oc import-image quay.io/btison/rhpam71-kieserver-openshift-gpte:1.1 -n openshift --confirm
```

To provision:
```
$ ansible-playbook playbooks/rhpam_dev.yml -e ocp_user=developer -e kieserver_image=rhpam71-kieserver-openshift-gpte
```