from EC2pricing.__init__ import result

from EC2pricing.StaticParameters import (
       EC2_REGIONS,
       EC2_DURATION_TERMS,
       EC2_OFFERING_CLASS,
       EC2_PURCHASE_OPTION
)

class EC2Price:
    # initialize the instance type and set the region
    def __init__(self):
        self.instance_data = result
        self.default_region = None

    def find_sku(self, **attributes):
        # convert to camel case
        camelcase_res = self.camelcase_conversion(attributes)
        # for debugging and check if the result is in correct format
        print(camelcase_res)
        # search for sku using instance_data
        print(self.instance_data)


    #convert the '_' to the camel case letters
    def camelcase_conversion(self, attributes):
        res = {}
        for attr_name, attr_value in attributes.items():
            if '_' in attr_name:
                attr_name = ''.join(char.capitalize() for char in attr_name.split('_'))
                attr_name = attr_name[0].lower()+attr_name[1:]
            res[attr_name] = attr_value
        return res



e = EC2Price()
e.find_sku(
  instance_type='c4.large',
  location='US East (N. Virginia)',
  operating_system='Linux'
)