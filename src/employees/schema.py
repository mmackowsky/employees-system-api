import graphene
from graphene_django import DjangoObjectType

from .models import Department, Employee


class DepartmentType(DjangoObjectType):
    class Meta:
        model = Department
        fields = '__all__'


class EmployeeType(DjangoObjectType):
    class Meta:
        model = Employee
        fields = '__all__'


class CreateEmployee(graphene.Mutation):
    class Arguments:
        first_name = graphene.String(required=True)
        surname = graphene.String(required=True)
        department = graphene.ID(required=True)

    employee = graphene.Field(EmployeeType)

    def mutate(self, info, first_name, surname, department):
        department = Department.objects.get(pk=department)
        employee = Employee(first_name=first_name, surname=surname, department=department)
        employee.save()
        return CreateEmployee(employee=employee)


class UpdateEmployee(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        department = graphene.ID(required=True)

    employee = graphene.Field(EmployeeType)

    def mutate(self, info, id, department=None):
        try:
            employee = Employee.objects.get(pk=id)
        except Employee.DoesNotExist:
            raise Exception("Employee does not exist")

        if department is not None:
            employee.department.id = department

        employee.save()
        return UpdateEmployee(employee=employee)


class DeleteEmployee(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        try:
            employee = Employee.objects.get(pk=id)
        except Employee.DoesNotExist:
            raise Exception("Employee does not exist")

        employee.delete()
        return DeleteEmployee(success=True)


class Query(graphene.ObjectType):
    employees = graphene.List(EmployeeType)
    employee = graphene.Field(EmployeeType, id=graphene.Int())
    department = graphene.List(DepartmentType)

    def resolve_employees(self, info):
        return Employee.objects.all()

    def resolve_employee(self, info, id):
        return Employee.objects.get(id=id)

    def resolve_department(self, info):
        return Department.objects.all()


class Mutation(graphene.ObjectType):
    create_employee = CreateEmployee.Field()
    update_employee = UpdateEmployee.Field()
    delete_employee = DeleteEmployee.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
