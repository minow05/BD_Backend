
from faker import Faker
from werkzeug.security import generate_password_hash
import random

def create_sample_data(app):
    """Funkcja generująca przykładowe dane"""
    with app.app_context():
        from models import db, Address, Employee, StudioHead, SectionManager, \
            TeamManager, TeamMember, Section, Team, TeamMembership, Game, Task, \
            SectionTask, TeamTask, EmployeeTask, TaskStatus
        db.drop_all()
        db.create_all()
        fake = Faker('pl_PL')
   
        addresses = []
        for _ in range(25):
            address = Address(
                city=fake.city(),
                street=fake.street_name(),
                postal_code=fake.postcode(),
                house_number=str(fake.random_int(min=1, max=200)),
                apartment_number=str(fake.random_int(min=1, max=80)) if fake.boolean(60) else None
            )
            addresses.append(address)
        
        db.session.add_all(addresses)
        db.session.commit()
      
        studio_head = StudioHead(
            first_name="Adam",
            last_name="Nowak",
            pesel=fake.pesel(),
            phone="+48" + fake.numerify("#########"),
            email="adam.nowak@gamestudio.pl",
            login="anowak",
            password_hash=generate_password_hash("StudioHead2024!"),
            hire_date="2018-03-15",
            fire_date=None,
            address_id=addresses[0].id
        )
        db.session.add(studio_head)
       
        section_managers = []
        sm_names = [
            ("Anna", "Kowalska"),
            ("Piotr", "Wiśniewski"),
            ("Magdalena", "Lewandowska")
        ]
        
        for i, (first_name, last_name) in enumerate(sm_names):
            manager = SectionManager(
                first_name=first_name,
                last_name=last_name,
                pesel=fake.pesel(),
                phone="+48" + fake.numerify("#########"),
                email=f"{first_name.lower()}.{last_name.lower()}@gamestudio.pl",
                login=f"{first_name[0].lower()}{last_name.lower()}",
                password_hash=generate_password_hash(f"SmPass{i+1}!"),
                hire_date=fake.date_between(start_date='-5y', end_date='-2y').strftime('%Y-%m-%d'),
                fire_date=None,
                address_id=addresses[i+1].id
            )
            section_managers.append(manager)
        
        db.session.add_all(section_managers)

        team_managers = []
        tm_names = [
            ("Krzysztof", "Jankowski"),
            ("Ewa", "Wójcik"),
            ("Michał", "Kowalczyk"),
            ("Karolina", "Kamińska"),
            ("Tomasz", "Zieliński"),
            ("Agnieszka", "Szymańska")
        ]
        
        for i, (first_name, last_name) in enumerate(tm_names):
            manager = TeamManager(
                first_name=first_name,
                last_name=last_name,
                pesel=fake.pesel(),
                phone="+48" + fake.numerify("#########"),
                email=f"{first_name.lower()}.{last_name.lower()}@gamestudio.pl",
                login=f"tm{i+1:02d}",
                password_hash=generate_password_hash(f"TmPass{i+1}!"),
                hire_date=fake.date_between(start_date='-3y', end_date='-1y').strftime('%Y-%m-%d'),
                fire_date=None,
                address_id=addresses[i+4].id
            )
            team_managers.append(manager)
        
        db.session.add_all(team_managers)
        
        team_members = []
        for i in range(10):
            first_name = fake.first_name()
            last_name = fake.last_name()
            member = TeamMember(
                first_name=first_name,
                last_name=last_name,
                pesel=fake.pesel(),
                phone="+48" + fake.numerify("#########"),
                email=f"member{i+1:02d}@gamestudio.pl",
                login=f"member{i+1:02d}",
                password_hash=generate_password_hash(f"Member{i+1}!"),
                hire_date=fake.date_between(start_date='-2y', end_date='today').strftime('%Y-%m-%d'),
                fire_date=fake.date_between(start_date='-6m', end_date='today').strftime('%Y-%m-%d') if fake.boolean(10) else None,
                address_id=addresses[i+10].id
            )
            team_members.append(member)
        
        db.session.add_all(team_members)
        db.session.commit()
       
        sections = []
        section_data = [
            "Programowanie",
            "Grafika 3D",
            "Grafika 2D",
            "Dźwięk",
            "Design",
            "QA"
        ]
        
        for i, name in enumerate(section_data):
            section = Section(
                name=name,
                manager_id=section_managers[i % len(section_managers)].id
            )
            sections.append(section)
        
        db.session.add_all(sections)
        db.session.commit()

        teams = []
        team_names = [
            "Silnik Gry",
            "AI System",
            "Fizyka",
            "Sieci",
            "UI/UX",
            "Shader Team",
            "Animacje",
            "Środowisko",
            "Postacie",
            "Audio Design",
            "Level Design",
            "Gameplay"
        ]
        
        for i, name in enumerate(team_names[:8]):  # 8 zespołów
            team = Team(
                name=name,
                section_id=sections[i % len(sections)].id,
                manager_id=team_managers[i % len(team_managers)].id
            )
            teams.append(team)
        
        db.session.add_all(teams)
        db.session.commit()
     
        memberships = []
        
        available_members = list(range(len(team_members)))
        random.shuffle(available_members)
        
        member_idx = 0
        for team in teams:
            num_members = random.randint(2, 4)
            for _ in range(num_members):
                if member_idx >= len(available_members):
                    break
                membership = TeamMembership(
                    team_member_id=team_members[available_members[member_idx]].id,
                    team_id=team.id
                )
                memberships.append(membership)
                member_idx += 1
        
        db.session.add_all(memberships)
        db.session.commit()

        games = []
        
        for i in range(0,2):  # 2 gry
            game = Game(
                studio_head_id=studio_head.id
            )
            games.append(game)
        
        db.session.add_all(games)
        db.session.commit()
        
        tasks = []
        task_descriptions = [
            "Implementacja systemu zapisu gry",
            "Optymalizacja renderowania terenu",
            "Stworzenie głównego menu UI",
            "Implementacja systemu dialogów NPC",
            "Tworzenie modelu głównego bohatera",
            "Animacje walki wręcz",
            "System pogody dynamicznej",
            "AI przeciwników podstawowych",
            "System umiejętności postaci",
            "Implementacja multiplayer PvP",
            "Tworzenie ścieżki dźwiękowej",
            "Efekty dźwiękowe broni",
            "Projektowanie pierwszego poziomu",
            "Testy balansu walki",
            "Implementacja sklepów w grze",
            "System osiągnięć",
            "Optymalizacja zużycia pamięci",
            "Tworzenie cutscenek",
            "System szybkiej podróży",
            "Implementacja minimapy"
        ]
        
        for i, desc in enumerate(task_descriptions):
            start_date = fake.date_between(start_date='-3m', end_date='today')
            end_date = fake.date_between(start_date='today', end_date='+6m')
            
            task = Task(
                description=desc,
                start_date=start_date.strftime('%Y-%m-%d'),
                end_date=end_date.strftime('%Y-%m-%d'),
                status=random.choice(list(TaskStatus))
            )
            tasks.append(task)
        
        db.session.add_all(tasks)
        db.session.commit()
        
        section_tasks = []
        
        for i, task in enumerate(tasks[:12]):  
            section_task = SectionTask(
                task_id=task.id,
                section_id=sections[i % len(sections)].id,
                game_id=games[i % len(games)].id
            )
            section_tasks.append(section_task)
        
        db.session.add_all(section_tasks)
        db.session.commit()
       
        team_tasks = []
        
        
        team_task = TeamTask(
            task_id=tasks[i].id,
            section_task_id=section_task.id,
            team_id=teams[i % len(teams)].id
        )
        team_tasks.append(team_task)
        
        db.session.add_all(team_tasks)
        db.session.commit()
      
        employee_tasks = []
        
        for team_task in team_tasks:
            # Znajdź członków tego zespołu
            team_id = team_task.team_id
            team_member_ids = [
                m.team_member_id for m in memberships 
                if m.team_id == team_id
            ]
            
          
            num_assignments = min(random.randint(1, 2), len(team_member_ids))
            selected_members = random.sample(team_member_ids, num_assignments)
            
            for member_id in selected_members:
                emp_task = EmployeeTask(
                    task_id=team_task.task_id,
                    team_task_id=team_task.id,
                    team_member_id=member_id
                )
                employee_tasks.append(emp_task)
        
        db.session.add_all(employee_tasks)
        db.session.commit()
        
        
        print("\nDANE LOGOWANIA DLA TESTÓW:")
        print("Studio Head:   login: anowak, password: StudioHead2024!")
        print("Section Manager 1: login: akowalska, password: SmPass1!")
        print("Team Manager 1:    login: tm01, password: TmPass1!")
        print("Team Member 1:     login: member01, password: Member1!")
        
        return True