from EC2pricing.__init__ import result

from EC2pricing.StaticParameters import (
       EC2_REGIONS,
       EC2_DURATION_TERMS,
       EC2_OFFERING_CLASS,
       EC2_PURCHASE_OPTION
)

class EC2Price:
    # initialize the instance_data using __init__.result and set the region to None
    def __init__(self):
        self.instance_data = result
        self.default_region = None

    def find_sku(self, **attributes):
        # Stores the result if Match is True
        Matched_attributes = set()
        # convert to camel case
        camelcase_res = self.camelcase_conversion(attributes)
        # for debugging and check if the result is in correct format
        print(camelcase_res)
        # search for sku using instance_data
        #print(self.instance_data)
        #boolean variable, set to False if there is no match
        Match = True
        '''
        Returns the sku (unique number for the service/instance type)
        iterate through the instance data and search for sku, productFamily
        if the productFamily attributes matches with the user attributes then add them to
        Matched_attributes set.

        '''
        for sku, productFamily in self.instance_data['products'].items():
             attributes = productFamily['attributes']
             for attr_name, attr_value in attributes.items():
                 if attributes.get(attr_name) != attr_value:
                     Match = False
                     break
             if Match == True:
                 Matched_attributes.add(sku)
        return Matched_attributes


    #convert the '_' to the camel case letters
    def camelcase_conversion(self, attributes):
        res = {}
        for attr_name, attr_value in attributes.items():
            if '_' in attr_name:
                attr_name = attr_name.split('_')
                attr_name = attr_name[0][0].lower()+attr_name[0][1:]+attr_name[1].capitalize()
                # attr_name = ''.join(char.capitalize() for char in attr_name.split('_'))
                # attr_name = attr_name[0].lower()+attr_name[1:]
            res[attr_name] = attr_value
        return res

    #get the sku from the args with unique results
    def get_sku(self, *args, **kwrags):
        # get the type of service (it's compute service for this API)
        product_family = kwrags.get('productfamily')
        # final result is stored in Matched_result
        Matched_result = {}
        #remove redundancy
        attribute_collision = set()
        #get the attributes to refine the sku search
        for sku, productFamily in self.instance_data['products'].items():
            if product_family is not None and product_family != productFamily:
                continue
            matched_attributes = [productFamily['attributes'][index_attr]
                                  for index_attr in args if index_attr in product_family['attributes']]
            hash_result = self.hash(*matched_attributes)
            if hash_result in Matched_result:
                attribute_collision.add(hash_result)
            if hash_result not in Matched_result:
                result[hash_result] = sku

        #returns the matched and unique result
        return result


    #hash function to remove the redundant results
    def __hash__(self, *args):
        return '|'.join(args)


#seperate class to compute the EC2 instances based on parameters
class ComputeEC2Price(EC2Price):
    def __init__(self, *args, **kwargs):
        self.operating_system = None,
        self.instancetype = 't2.micro',
        self.tenancy = 'Shared',
        self.preinstalledsoftware ='NA',
        self.region = None

        #get the sku number out of the above combination
        self.sku = self.get_sku(
            'instanceType', 'operatingSystem', 'tenancy', 'preInstalledSoftware','location',
            productfamily = 'Compute Instance'
        )

    #get the ondemand instances pricing
    def onDemandInstance(self, instance_type,
                         operating_system = None,
                         tenancy = None,
                         preinstalledsoftware = None,
                         region = None):



    #get the reserved insatnces


    #get the sku based on default or user passed values



    #get the sku based on the
e = EC2Price()
e.find_sku(
  instance_type='c4.large',
  location='US East (N. Virginia)',
  operating_system='Linux'
)