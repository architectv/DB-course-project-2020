# from django.test import TestCase
# from .models import User, Project, Task
# from django.contrib.auth.models import User


# class ProfileTests(TestCase):
#     def test_create_profile(self):
#         user = User.objects.create_user('jack')
#         profile = Profile.objects.create(user=user)
#         self.assertEqual(str(profile), 'jack')


# class ProjectTests(TestCase):
#     def test_change(self):
#         user = User.objects.create_user('jack')
#         profile = Profile.objects.create(user=user)

#         project = Project.objects.create(
#             title='Test Title',
#             description='Test Description',
#             author=profile,
#         )
#         project.add_member(profile)

#         # Change title & description
#         self.assertEqual(project.title, 'Test Title')
#         self.assertEqual(project.description, 'Test Description')

#         project.change_title('New Title')
#         project.change_description('New Description')

#         self.assertEqual(project.title, 'New Title')
#         self.assertEqual(project.description, 'New Description')

#         user2 = User.objects.create_user('kevin')
#         profile2 = Profile.objects.create(user=user2)

#         # Add member
#         project.add_member(profile2)

#         projects2 = Project.own.all(id=profile2.id)[:]
#         self.assertEqual(len(projects2), 1)
#         self.assertEqual(projects2[0], project)

#         # Delete project
#         project.delete()
#         projects = Project.own.all(id=profile.id)[:]
#         projects2 = Project.own.all(id=profile2.id)[:]
#         self.assertEqual(len(projects), 0)
#         self.assertEqual(len(projects2), 0)


# class TaskTests(TestCase):
#     def test_change(self):
#         user = User.objects.create_user('jack')
#         profile = Profile.objects.create(user=user)

#         user2 = User.objects.create_user('kevin')
#         profile2 = Profile.objects.create(user=user2)

#         user3 = User.objects.create_user('donald')
#         profile3 = Profile.objects.create(user=user3)

#         project = Project.objects.create(
#             title='Test Title',
#             description='Test Description',
#             author=profile,
#         )
#         project.members.add(profile, profile2, profile3)

#         # Create task
#         task = Task.objects.create(
#             title='Test Task',
#             description='To do something...',
#             project=project,
#             author=profile,
#             performer=profile2,
#         )

#         self.assertEqual(task.title, 'Test Task')
#         self.assertEqual(task.description, 'To do something...')
#         self.assertEqual(task.author, profile)
#         self.assertEqual(task.performer, profile2)

#         # Change task
#         task.change_performer(profile3)
#         task.change_title('New Title')
#         task.change_description('New Description')

#         self.assertEqual(task.performer, profile3)
#         self.assertEqual(task.title, 'New Title')
#         self.assertEqual(task.description, 'New Description')

#         # Delete task
#         task.delete()
#         tasks = Task.own.all(performer_id=profile3.id)[:]
#         self.assertEqual(len(tasks), 0)
