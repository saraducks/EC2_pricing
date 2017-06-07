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
        # convert to camel case
        camelcase_res = self.camelcase_conversion(attributes)
        # Stores the result if Match is True
        Matched_attributes = set()
        # for debugging and check if the result is in correct format
        #print(camelcase_res)
        # search for sku using instance_data
        #print(self.instance_data)
        #boolean variable, set to False if there is no match
        '''
        Returns the sku (unique number for the service/instance type)
        iterate through the instance data and search for sku, productFamily
        if the productFamily attributes matches with the user attributes then add them to
        Matched_attributes set.

        '''
        for sku, productFamily in self.instance_data['products'].items():
             attributes = productFamily['attributes']
             Match = True
             for attr_name, attr_value in camelcase_res.items():
                 if not attributes.get(attr_name) == attr_value:
                     Match = False
                     break
             if Match:
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
                         preinstalled_software = None,
                         region = None):
        ondemand_sku = self.retrive_sku(
            instance_type = instance_type,
            operating_system = operating_system,
            tenancy = tenancy,
            preinstalled_software = preinstalled_software,
            region = region
        )
        term = self.instance_data['terms']['OnDemand'][ondemand_sku]
        price_dimensions = next(term.items())['priceDimensions']
        price_dimension = next(price_dimensions.items())
        raw_price = price_dimension['pricePerUnit']['USD']
        return float(raw_price)

    #get the reserved instances
    def reservedInstances(self,
                          instance_type,
                          operating_system = None,
                          tenancy = 'Shared',
                          preinstalled_software = None,
                          offering_class= None,
                          lease_contract_length = None,
                          purcahse_option= None,
                          region = None):
        # get the sku for the reserved instances
        reserved_sku = self.retrive_sku(
            instance_type,
            operating_system=operating_system,
            tenancy=tenancy,
            preinstalledsoftware= preinstalled_software,
            region=region)

        # length of the period you need instances
        duration_attributes = [
            purcahse_option,
            offering_class,
            lease_contract_length
        ]

        reserved_offerterm_result = self.get_reserved_offerterm(reserved_sku, duration_attributes)

    # To return thr matching offer terms for reserved instances
    def get_reserved_offerterm(self, *term_attributes, **kwargs):
        '''
        get the reserved term attributes first
        Filter the reserved term attributes based on tern_attributes
        returns the filtered reserved offerTerm from JSON file

        '''

    #get the sku based on default or user passed values
    def retrive_sku(self, instance_type,
                    operating_system = None,
                    tenancy = None,
                    preinstalledsoftware = None,
                    region = None ):
         if instance_type == None:
             instance_type = self.instancetype
         if region == None:
             region = self.region
         if not region:
             raise ValueError("no such region defined ")
         if region in EC2_REGIONS:
             region = EC2_REGIONS[region]
         tenancy = tenancy or self.tenancy
         preinstalledsoftware = preinstalledsoftware or self.preinstalledsoftware

         attributes = [instance_type, region, tenancy, preinstalledsoftware]

         result_sku = self.sku.get(*attributes)
         if result_sku is None:
             raise ValueError("Unable to lookup SKU for attributes: {}"
                              .format(attributes))
         return result_sku



# e = EC2Price()
# e.find_sku(
#   instance_type='c4.large',
#   location='US East (N. Virginia)',
#   operating_system='Linux'
# )