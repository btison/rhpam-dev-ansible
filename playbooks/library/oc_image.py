#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.openshift import Utils
from ansible.module_utils.openshift import OpenShiftCLI

class OCImage(OpenShiftCLI):
    ''' Class to import and create an imagestream object'''
    def __init__(self,
                 namespace,
                 registry_url,
                 image_name,
                 image_tag,
                 kubeconfig='/etc/origin/master/admin.kubeconfig',
                 verbose=False):
        ''' Constructor for OCImage'''
        super(OCImage, self).__init__()
        self.namespace = namespace
        self.registry_url = registry_url
        self.image_name = image_name
        self.image_tag = image_tag
        self.verbose = verbose

    def get(self):
        '''return a image by name '''
        results = self._get('imagestream', self.image_name)
        results['exists'] = False
        if results['returncode'] == 0 and results['results'][0]:
            results['exists'] = True

        if results['returncode'] != 0 and '"{}" not found'.format(self.image_name) in results['stderr']:
            results['returncode'] = 0

        return results

    def create(self, url=None, name=None, tag=None):
        '''Create an image '''
        return self._import_image(url, name, tag)


    # pylint: disable=too-many-return-statements
    @staticmethod
    def run_ansible(params, check_mode):
        ''' run the oc_image module'''

        ocimage = OCImage(params['namespace'],
                          params['registry_url'],
                          params['image_name'],
                          params['image_tag'],
                          kubeconfig=params['kubeconfig'],
                          verbose=params['debug'])

        state = params['state']

        api_rval = ocimage.get()

        #####
        # Get
        #####
        if state == 'list':
            if api_rval['returncode'] != 0:
                return {"failed": True, "msg": api_rval}
            return {"changed": False, "ansible_module_results": api_rval, "state": "list"}

        ########
        # Create
        ########
        if state == 'present':

            if not Utils.exists(api_rval['results'], params['image_name']):

                if check_mode:
                    return {"changed": False, "msg": 'CHECK_MODE: Would have performed a create'}

                api_rval = ocimage.create(params['registry_url'],
                                          params['image_name'],
                                          params['image_tag'])

                if api_rval['returncode'] != 0:
                    return {"failed": True, "msg": api_rval}

                # return the newly created object
                api_rval = ocimage.get()

                if api_rval['returncode'] != 0:
                    return {"failed": True, "msg": api_rval}

                return {"changed": True, "ansible_module_results": api_rval, "state": "present"}

            # image exists, no change
            return {"changed": False, "ansible_module_results": api_rval, "state": "present"}

        return {"failed": True, "changed": False, "msg": "Unknown state passed. {0}".format(state)}

    def _import_image(self, url=None, name=None, tag=None):
        ''' perform image import '''
        cmd = ['import-image']

        image = '{0}'.format(name)
        if tag: 
            image += ':{0}'.format(tag)

        cmd.append(image)

        if url: 
            cmd.append('--from={0}/{1}'.format(url, image))

        cmd.append('-n{0}'.format(self.namespace))

        cmd.append('--confirm')
        return self.openshift_cmd(cmd)


def main():
    '''  
    ansible oc module for image import
    '''

    module = AnsibleModule(
        argument_spec=dict(
            kubeconfig=dict(default='/etc/origin/master/admin.kubeconfig', type='str'),
            state=dict(default='present', type='str',
                       choices=['present', 'list']),
            debug=dict(default=False, type='bool'),
            namespace=dict(default='default', type='str'),
            registry_url=dict(default=None, type='str'),
            image_name=dict(default=None, required=True, type='str'),
            image_tag=dict(default=None, type='str'),
            force=dict(default=False, type='bool'),
        ),   

        supports_check_mode=True,
    )    

    rval = OCImage.run_ansible(module.params, module.check_mode)

    if 'failed' in rval:
        module.fail_json(**rval)

    module.exit_json(**rval)

if __name__ == '__main__':
    main()
