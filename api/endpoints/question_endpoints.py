from data_loader.models import Person, Fruit, Vegetable
from api.serializers import PersonSerializer


class QuestionOne:
    """
    Given a company, the API needs to return all their employees. Provide the appropriate solution
    if the company does not have any employees.
    """

    def get_response(self, company_index):
        """
        API to return all the employees of a company.
        :param company_index: int (company_index)
        :return: serialized person objects
        """
        people_working_in_company = Person.objects.filter(company_id__index=company_index).all()

        if not people_working_in_company:
            return {
                'response': f"No employees found for company index: {company_index}"
            }

        serializer = PersonSerializer(people_working_in_company, many=True)
        return serializer.data


class QuestionTwo:
    """
    Given 2 people, provide their information (Name, Age, Address, phone) and the
    list of their friends in common which have brown eyes and are still alive.
    """
    def get_response(self, person_1, person_2):
        """

        :param request:
        :return:
        """
        person1_obj = Person.objects.filter(
            index=person_1
        ).first()
        person2_obj = Person.objects.filter(
            index=person_2
        ).first()

        if person1_obj is None or person2_obj is None:
            return {
                'error': 'person does not exist'
            }

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


class QuestionThree:
    def get_response(self, person_index):
        person_obj = Person.objects.filter(
            index=int(person_index)
        ).first()

        if person_obj is None:
            return {'error': 'Person does not exist'}

        fruits_list = []
        vegetables_list = []
        fruits = Fruit.objects.filter(person=person_obj)
        if fruits:
            fruits_list = [fruit.fruit_name for fruit in fruits]

        vegetables = Vegetable.objects.filter(person=person_obj)
        if vegetables:
            vegetables_list = [vege.vegetable_name for vege in vegetables]

        final_response = {
            "username": person_obj.name,
            "age": person_obj.age,
            "fruits": fruits_list,
            "vegetables": vegetables_list
        }
        return final_response
