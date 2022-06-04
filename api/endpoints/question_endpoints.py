from data_loader.models import Person
from api.serializers import PersonSerializer

class QuestionOne:

    def get_response(self, request, company_index):
        serializer_context = {
            'request': request,
        }
        id = company_index
        people_working_in_company = Person.objects.filter(company_id__index=id)
        if not people_working_in_company:
            return {
                'response': f"No employees found for company index: {company_index}"
            }
        serializer = PersonSerializer(people_working_in_company, many=True, context=serializer_context)
        return serializer.data


class QuestionTwo:

    def get_response(self, request):
        person1_obj = Person.objects.get(
            index=int(request.query_params.get('person1'))
        )
        person2_obj = Person.objects.get(
            index=int(request.query_params.get('person2'))
        )
        color = 'brown'
        final_list = []
        for i in Person.objects.raw(
            'select ip.id, ip.name from data_loader_person p '
            'join data_loader_personfriend pf on p.id=pf.person_id_id '
            'join data_loader_person ip on ip.id=pf.friend_id_id '
            'where p.name in (%s, %s) '
            'and ip.eye_color=%s and ip.has_died=0 group by ip.id', [person1_obj.name, person2_obj.name, color]
        ):
            final_list.append(i.name)
        final_response = [
            {
                "Name": person1_obj.name,
                "Age": person1_obj.age,
                "Address": person1_obj.address,
                "Phone": person1_obj.phone
            },
            {
                "Name": person2_obj.name,
                "Age": person2_obj.age,
                "Address": person2_obj.address,
                "Phone": person2_obj.phone
            },
            {
                "common_friends": final_list
            }
        ]
        return final_response

