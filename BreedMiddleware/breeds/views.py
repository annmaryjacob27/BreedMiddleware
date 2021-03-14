import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from asgiref.sync import async_to_sync


class LongestBreeds(APIView):
    """
    LongestBreeds
    """
    def get(self, request):
        """
        http://<domain>/api/longest-lifespan-breed/?breed_group=Terrier api calls comes here
        this functions takes the breed_group from the query and get the list of breeds
        of same breed group. then finds the breed with longest life span.
        then with the image id of the longest lifespan breed, gets the image url and
        process the data to return
        """
        data = {}
        try:
            breed_group = request.GET.get('breed_group', False)
            if breed_group:
                all_breeds = self.get_breed_group(breed_group)
                if all_breeds:
                    longest_lifespan = self.get_longest_lifespan_breed(all_breeds)
                    if longest_lifespan:
                        breed_image = self.get_breed_image(longest_lifespan)
                        # this data dict will prepare if there is no data in breed_image, respective fileds will be empty 
                        # in the dict
                        data = {
                            'name': longest_lifespan.get('name', ''),
                            'bred_for': longest_lifespan.get('bred_for', ''),
                            'breed_group': longest_lifespan.get('breed_group', ''),
                            'temperament': longest_lifespan.get('temperament', ''),
                            'image': {
                                'url': breed_image.get('url', ''),
                                'height': breed_image.get('height', ''),
                                'width': breed_image.get('width', ''),
                            }
                        }
                    else:
                        data = {
                            'status': "error",
                            'message': "Breeds with life span not found"
                        }
                else:
                    data = {
                        'status': "error",
                        'message': "Selected breed_group not found"
                    }
            else:
                data = {
                    'status': "error",
                    'message': "Invalid query parameter. Please check the format:http://<domain>/api/breeds/?breed_group=Toy"
                }
        except Exception as e:
            print(e)
            data = {
                'status': "error",
                'message': "Internal server Error: Please contact Admin"
            }
        return Response(data, status=status.HTTP_200_OK)
    
    @async_to_sync
    async def get_breed_group(self, breed_group): 
        """
        async function that makes the api call to get all breeds of a particular breed_group
        as the requirment
        """
        url = 'https://api.thedogapi.com/v1/breeds/search/?name={}'.format(breed_group) 
        response = requests.get(url) 
        data = response.json()
        return data

    
    def get_longest_lifespan_breed(self, all_breeds):
        """
        sorting and getting the breed with longest life span.
        if life span is range like 10-12years, then
        the avergae is taken and sorted and the first breed to returned
        
        """
        filtered_breeds = self.get_filter_breeds(all_breeds)
        if filtered_breeds:
            sorted_breeds = sorted(filtered_breeds, 
            key=lambda k: sum([int(i) for i in k['life_span'].split() if i.isdigit()])/len([int(i) 
            for i in k['life_span'].split() if i.isdigit()]), reverse=True)
        if sorted_breeds:
            return sorted_breeds[0]
        return {}
    
    def get_breed_image(self, breed):
        """
        functions that makes the api call to get the breed image url
        """
        image_id =  breed.get('reference_image_id', False)
        if image_id:
            url = 'https://api.thedogapi.com/v1/images/{}'.format(image_id)
            response = requests.get(url) 
            data = response.json()
            return data
        return {}
    
    def get_filter_breeds(self, breeds):
        """
        function to filter the breed list, if the a breed doesnot have an attribute life span
        """
        return [each for each in breeds if each.get('life_span', False)]

