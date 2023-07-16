import json
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from .models import Register,TodoTask
import re
from datetime import datetime


def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        phoneno = data.get('phoneno')
        password = data.get('password')

        if not username or not email or not phoneno or not password:
            return JsonResponse({'message': 'All fields are required. Please enter again!!'}, status=400)

        if not re.match(r'^\d{10}$', phoneno):
            return JsonResponse({'message': 'Phone number must be 10 digits. Please enter again!!'}, status=400)

        if not re.match(
                r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$',
                password
        ):
            return JsonResponse(
                {
                    'message': 'Invalid password. Password must contain at least one uppercase letter, one lowercase letter, '
                               'one special character, and be at least 8 characters long.'
                },
                status=400
            )

        if Register.objects.filter(email=email).exists():
            return JsonResponse({'message': 'Email already exists'}, status=400)
        else:
            register = Register.objects.create(
                username=username,
                email=email,
                phoneno=phoneno,
                password=make_password(password)
            )

        return JsonResponse({'message': 'Registration successful'})

    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)



def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data['email']
        password = data['password']

        register = Register.objects.filter(email=email, val=0).first()

        if register:
            if check_password(password, register.password):
                # if TodoTask.objects.filter(username_id=register.id).exists():
                #     tasks = TodoTask.objects.filter(username_id=register.id)
                register.val = 1
                register.save()
                

                    # task_data = []
                    # for task in tasks:
                    #     task_data.append({'id': task.id, 'task': task.taskTest})


                    # return JsonResponse({'message': 'Login successful', 'id': register.id, 'tasks': task_data})
                

                return JsonResponse({'message': 'Login successful', 'id': register.id})

            else:
                return JsonResponse({'message': 'Invalid password'}, status=400)

        return JsonResponse({'message': 'Invalid email or already logged in'}, status=400)

    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)
 




def logout(request):
    if request.method == 'POST':
        data = json.loads(request.body)
       # logout = data['email']
        user_id = data['loginid']
        #password = data['password']

        register = Register.objects.filter(id=user_id,val=1).first()

        if register:
            # if check_password(register.password):
            #     if Register.objects.filter(email=email,val=0).exists():
            #         return JsonResponse({'message': 'You are not loggged in'}, status=400)
                
                register.val = 0
                register.save()

                return JsonResponse({'message': 'Logout successful'})
        

            # else:
            #     return JsonResponse({'message': 'Invalid password'}, status=400)

        return JsonResponse({'message': 'already logged out'}, status=400)

    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)
    









def todo(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        taskTest = data['taskText']
        id = data['id']

        register = Register.objects.filter(id=id).first()

        if register:
            todo = TodoTask.objects.create(
                taskTest=taskTest,
            #     createdTime=datetime.now(),
                  #updatedTime=datetime.now(),
                 # checkedTime=datetime.now(),
                #  deletedTime=datetime.now(),
                username=register,
               # serial=0,
                status_c=False,
                status_d=False
            )
            return JsonResponse({'task_id': todo.id,'status':False,'taskText' : taskTest,'message': 'Todo saved successfully'})
        else:
            return JsonResponse({'message': 'User not logged in'}, status=400)
    





    if request.method == 'GET':
        id = request.GET.get('loginid')
        if not id:
          return JsonResponse({'message': 'id required'}, status=400)
     

        if TodoTask.objects.filter(username_id=id).exists():
          tasks = TodoTask.objects.filter(username_id=id,status_d=0)

          task_data = []
          for task in tasks:
              task_data.append({'task_id': task.id,'status':False,'taskText': task.taskTest})

          return JsonResponse({'id':id,'task': task_data})
        else:
            return JsonResponse({'message':  'No tasks found for the provided login ID'}, status=200)
    
   


        

    

    
    if request.method == 'PUT':
        data = json.loads(request.body)
        id = data['task_id']
        update = data['update']
        todo=TodoTask.objects.filter(id=id).first()
        if todo:
            todo.taskTest = update
            todo.updatedTime = datetime.now()

            todo.save()
        return JsonResponse({'task_id': todo.id,'message': 'Updated successfully'})        

    



    if request.method == 'DELETE':
        data = json.loads(request.body)
        id = data['task_id']
        status = data['status']
        if status == "deleted" :
             todo = TodoTask.objects.filter(id=id).first()
             if todo:
               todo.status_d = '1'
               todo.deletedTime = datetime.now()
               todo.save()
               return JsonResponse({'status':'deleted'})
        elif status == "completed":
             todo = TodoTask.objects.filter(id=id).first()
             if todo:
               todo.status_c = '1'
               todo.checkedTime = datetime.now()
               todo.save()
               return JsonResponse({'status':'completed'})
        else:
            return JsonResponse({'message': 'Invalid status'}, status=400)
    
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)
    

# # def todoedit(request):
# #     if request.method == 'POST':
# #         data = json.loads(request.body)
# #         taskTest = data['taskTest']
# #         serial = data['serial']
    


# #         register = Register.objects.filter(val=1).first()

# #         if register:
# #             todo = Todo.objects.filter(username_id=register.id, serial=serial).first()
# #             if todo:
# #                 todo.taskTest = taskTest
# #                 todo.updatedTime = datetime.now()
# #                 todo.save()

# #                 return JsonResponse({'message': 'todo saved successfully'})
# #             else:
# #                 return JsonResponse({'message': 'Todo not found'}, status=404)
        
        
# #         if register:
# #             todo = Todo.objects.filter(username_id=register.id, serial=serial).first()
# #             if todo:
# #                # todo.status = status
# #                 todo.checkedTime = datetime.now()
# #                 todo.save()

# #                 return JsonResponse({'message': 'completed status saved successfully'})
# #             else:
# #                 return JsonResponse({'message': 'Todo not found'}, status=404)
# #         else:
# #             return JsonResponse({'message': 'User not logged in'}, status=400)

# #     else:
# #         return JsonResponse({'message': 'Invalid request method'}, status=405)
    
# def savetodos(request):
#     if request.method == 'POST':
#         todos_json = json.loads(request.body)
        
#         for todo_json in todos_json:
#             task_text = todo_json['taskText']
#             order_id = todo_json['orderId']
#             status = todo_json['status']
            
#             if status == 'deleted':
#                 todo = TodoTask.objects.filter(taskTest=task_text, serial=order_id).first()
#                 if todo:
#                     todo.status_d = True
#                     todo.deletedTime = datetime.now()
#                     todo.save()
#             else:
#                 todo, created = TodoTask.objects.get_or_create(taskTest=task_text, serial=order_id)
                
#                 if created:
#                     todo.createdTime = datetime.now()
                
#                 if status == 'completed':
#                     todo.status_c = True
#                     todo.checkedTime = datetime.now()
#                 else:
#                     todo.status_c = False
#                     todo.updatedTime = datetime.now()
                
#                 todo.save()
        
#         return JsonResponse({'message': 'Todo list data saved successfully'})
#     else:
#         return JsonResponse({'message': 'Invalid request method'})




# def login(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         email = data['email']
#         password = data['password']

#         register = Register.objects.filter(email=email, val=0).first()

#         if register:
#             if check_password(password, register.password):
#                 if Register.objects.filter(val=1).exists():
#                       return JsonResponse({'message': 'Another user is already logged in'}, status=400)

#                 register.val = 1
#                 register.save()

#                 return JsonResponse({'message': 'Login successful','id': register.id})

#             else:
#                 return JsonResponse({'message': 'Invalid password'}, status=400)

#         return JsonResponse({'message': 'Invalid email or already logged in'}, status=400)

#     else:
#         return JsonResponse({'message': 'Invalid request method'}, status=405)

# def login(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         email = data['email']
#         password = data['password']

#         register = Register.objects.filter(email=email, val=1).first()

#         if register:
#             if check_password(password, register.password):
#                 if Register.objects.filter(val=1).exists():
#                     todo_task = TodoTask.objects.filter(user_id=register.id).first()
#                     if todo_task:
#                         task_tests = todo_task.taskTest.all()
#                         task_test_fields = [task.test_field_name for task in task_tests]
#                         return JsonResponse({'message': 'Another user is already logged in', 'id': register.id, 'task': task_test_fields}, status=400)
#                     else:
#                         return JsonResponse({'message': 'Another user is already logged in', 'id': register.id}, status=400)

#                 register.val = 1
#                 register.save()

#                 return JsonResponse({'message': 'Login successful', 'id': register.id})

#             else:
#                 return JsonResponse({'message': 'Invalid password'}, status=400)

#         return JsonResponse({'message': 'Invalid email or already logged in'}, status=400)

#     else:
#         return JsonResponse({'message': 'Invalid request method'}, status=405)




# def logout(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         email = data['email']
#         password = data['password']

#         register = Register.objects.filter(email=email,val=1).first()

#         if register:
#             if check_password(password, register.password):
#                 if Register.objects.filter(email=email,val=0).exists():
#                     return JsonResponse({'message': 'You are not loggged in'}, status=400)

#                 register.val = 0
#                 register.save()

#                 return JsonResponse({'message': 'Logout successful'})
        

#             else:
#                 return JsonResponse({'message': 'Invalid password'}, status=400)

#         return JsonResponse({'message': 'already logged out'}, status=400)

#     else:
#         return JsonResponse({'message': 'Invalid request method'}, status=405)
    
# [{"taskText":"code","status":false,"editMode":false},{"taskText":"Eat","status":"deleted","editMode":false,"checkedTime":"13/07/2023, 18:19:40"},{"taskText":"jhj","status":false,"editMode":false,"updatedText":"jhj"},{"taskText":"asdsa","status":"completed","editMode":false,"checkedTime":"13/07/2023, 18:19:35"}]
