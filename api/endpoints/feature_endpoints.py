from data_loader.models import Person, Fruit, Vegetable, PersonFriend
from api.serializers import PersonSerializer


class AllCompanyEmployees:
    """
    Given a company, the API needs to return all their employees. Provide the appropriate solution
    if the company does not have any employees.
    """

    def get_response(self, company_index):
        """
        To get all the employees of a company.
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


class CommonPeople:
    """
    Given 2 people, provide their information (Name, Age, Address, phone) and the
    list of their friends in common which have brown eyes and are still alive.
    """
    def get_response(self, person_1, person_2) -> dict:
        """
        Get the two person index, run a query and return the result with the person details
        and their common friends who have brown eye and are alive

        :param person_1: int, person_index
        :param person_2: int, person_index
        :return: dict
        """
        # query and load the 2 people
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

        # constaint given in the question
        color = 'brown'
        has_died = 0

        final_list = []
        try:
            for person in Person.objects.raw(
                'select per.id, per.name from '
                '(select t1.id as skip, t1.friend_id as id from '
                '(SELECT pf.id as id, pf.friend_id_id as friend_id FROM data_loader_person p '
                'join data_loader_personfriend pf on pf.person_id_id=p.id '
                'join data_loader_person dpl on dpl.id=pf.friend_id_id '
                'where p.name = %s and dpl.eye_color=%s and dpl.has_died=%s ) t1 '
                'join '
                '(SELECT pf.id as id, pf.friend_id_id as friend_id FROM data_loader_person p '
                'join data_loader_personfriend pf on pf.person_id_id=p.id '
                'join data_loader_person dpl on dpl.id=pf.friend_id_id '
                'where p.name = %s ) t2 on t1.friend_id=t2.friend_id) t3 '
                'join data_loader_person per on per.id=t3.id;', [person1_obj.name, color, has_died, person2_obj.name]
            ):
                final_list.append(person.name)
        except Exception as e:
            print(e)

        # create the response structure
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


class FavoriteFruitsVeges:
    """
    Given 1 people, provide a list of fruits and vegetables they like. This endpoint must respect
    this interface for the output:
    {
        "username": "Ahi",
        "age": "30",
        "fruits": ["banana", "apple"],
        "vegetables": ["beetroot", "lettuce"]
    }
    """
    def get_response(self, person_index) -> dict:
        """
        Using the person_index, query the person then query the person's favorite fruits
        and vegetables and return them in a list

        :param person_index:int
        :return: dict
        """
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
