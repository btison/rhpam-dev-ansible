Ansible playbook for provisioning RHPAM (Business Central + KIE Server + Postgres)

Prerequisites:
* Log in into Openshift as admin user.

Provision:
```
$ ansible-playbook playbooks/pgadmin4.yml -e ocp_user=user1
$ ansible-playbook playbooks/nexus2.yml -e ocp_user=user1
$ ansible-playbook playbooks/rhpam_dev.yml -e ocp_user=user1 -e kieserver_image=rhpam71-kieserver-openshift-gpte -e kieserver_image_tag=1.1-3 -e businesscentral_image=rhpam71-businesscentral-openshift-gpte -e businesscentral_image_tag=1.1  
```

Provision for a range of users:
```
$ ansible-playbook playbooks/install.yml -e seq_start=1 -e seq_end=10
```

__Using custom images for Business-Central and KIE Server__
* Import image into openshift namespace:
```
$ oc import-image quay.io/btison/rhpam71-kieserver-openshift-gpte:1.1-3 -n openshift --confirm
```
```
$ oc import-image quay.io/btison/rhpam71-businesscentral-openshift-gpte:1.1 -n opensh
```
* Provision:
```
$ ansible-playbook playbooks/pgadmin4.yml -e ocp_user=user1
$ ansible-playbook playbooks/nexus2.yml -e ocp_user=user1
$ ansible-playbook playbooks/rhpam_dev.yml -e ocp_user=user1 -e kieserver_image=rhpam71-kieserver-openshift-gpte -e kieserver_image_tag=1.1-3 -e businesscentral_image=rhpam71-businesscentral-openshift-gpte -e businesscentral_image_tag=1.1
```
* Provision for a range of users:
```
$ ansible-playbook playbooks/install.yml -e seq_start=1 -e seq_end=10 -e kieserver_image=rhpam71-kieserver-openshift-gpte -e kieserver_image_tag=1.1-3 -e businesscentral_image=rhpam71-businesscentral-openshift-gpte -e businesscentral_image_tag=1.1
```