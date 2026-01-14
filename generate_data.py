from faker import Faker
from werkzeug.security import generate_password_hash
import random
from datetime import datetime

def create_sample_data(app):
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
        for i in range(15):
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
        
        for i, name in enumerate(team_names[:8]):
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

        game = Game(
            studio_head_id=studio_head.id
        )
        db.session.add(game)
        db.session.commit()

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
            "Implementacja minimapy",
            "Implementacja systemu czatowania",
            "Optymalizacja ładowania tekstur",
            "Stworzenie systemu osiągnięć",
            "Implementacja mikrotransakcji",
            "Tworzenie systemu przygód pobocznych",
            "Balansowanie trudności",
            "Implementacja trybu współpracy",
            "Tworzenie edytora poziomów",
            "System zapisu postępu",
            "Implementacja leaderboardów"
        ]
        
        section_tasks = []

        for i, section in enumerate(sections):
            num_section_tasks = random.randint(2, 3)
            
            for j in range(num_section_tasks):
                desc_idx = (i * 3 + j) % len(task_descriptions)
                task = Task(
                    description=f"[SEKCJA] {task_descriptions[desc_idx]}",
                    start_date=fake.date_between(start_date='-3m', end_date='today').strftime('%Y-%m-%d'),
                    end_date=fake.date_between(start_date='today', end_date='+6m').strftime('%Y-%m-%d'),
                    status=random.choice(list(TaskStatus))
                )
                db.session.add(task)
                db.session.flush() 
                section_task = SectionTask(
                    task_id=task.id,
                    section_id=section.id,
                    game_id=game.id
                )
                section_tasks.append(section_task)
        
        db.session.add_all(section_tasks)
        db.session.commit()

        team_tasks = []

        for i, team in enumerate(teams):
            num_team_tasks = random.randint(3, 5)
            
            for j in range(num_team_tasks):
                desc_idx = (i * 5 + j + 10) % len(task_descriptions) 
                task = Task(
                    description=f"[ZESPÓŁ {team.name}] {task_descriptions[desc_idx]}",
                    start_date=fake.date_between(start_date='-2m', end_date='today').strftime('%Y-%m-%d'),
                    end_date=fake.date_between(start_date='today', end_date='+3m').strftime('%Y-%m-%d'),
                    status=random.choice(list(TaskStatus))
                )
                db.session.add(task)
                db.session.flush()

                matching_section_tasks = [st for st in section_tasks if st.section_id == team.section_id]
                section_task_for_team = random.choice(matching_section_tasks) if matching_section_tasks else None

                team_task = TeamTask(
                    task_id=task.id,
                    section_task_id=section_task_for_team.id if section_task_for_team else None,
                    team_id=team.id
                )
                team_tasks.append(team_task)
        
        db.session.add_all(team_tasks)
        db.session.commit()

        employee_tasks = []

        team_member_with_team = {}
        for membership in memberships:
            if membership.team_member_id not in team_member_with_team:
                team_member_with_team[membership.team_member_id] = []
            team_member_with_team[membership.team_member_id].append(membership.team_id)

        for member_id, team_ids in team_member_with_team.items():
            num_employee_tasks = random.randint(1, 3)
            
            for j in range(num_employee_tasks):

                team_id = random.choice(team_ids)

                team_tasks_for_team = [tt for tt in team_tasks if tt.team_id == team_id]
                
                if team_tasks_for_team:
                    team_task = random.choice(team_tasks_for_team)
                    
                    task = Task(
                        description=f"[PRACOWNIK] Szczegół: {task_descriptions[(member_id + j) % len(task_descriptions)]}",
                        start_date=fake.date_between(start_date='-1m', end_date='today').strftime('%Y-%m-%d'),
                        end_date=fake.date_between(start_date='today', end_date='+1m').strftime('%Y-%m-%d'),
                        status=random.choice(list(TaskStatus))
                    )
                    db.session.add(task)
                    db.session.flush()
                    

                    emp_task = EmployeeTask(
                        task_id=task.id,  
                        team_task_id=team_task.id,
                        team_member_id=member_id
                    )
                    employee_tasks.append(emp_task)
        
        db.session.add_all(employee_tasks)
        db.session.commit()
        
        return True
