async function genNav(position)
                {
                    
                    nav = document.getElementById("nav")

                    if (position == "employee")
                    nav.innerHTML = `<button class = "nav-button" onclick="chooseOption('main')">Główna strona</button>
                <button class = "nav-button" onclick="chooseOption('data')">Wyświetl dane użytkownika</button>
                <button class = "nav-button" onclick="chooseOption('task')">Wyświetl swoje zadania</button>`
                    else if (position == "teamManager")
                    nav.innerHTML = `<button class = "nav-button" onclick="chooseOption('main')">Główna strona</button>
                <button class = "nav-button" onclick="chooseOption('data')">Wyświetl dane użytkownika</button>
                <button class = "nav-button" onclick="chooseOption('task')">Wyświetl swoje zadania</button>
                <button class = "nav-button" onclick="chooseOption('employee-task')">Wyświetl zadania pracowników</button>
                <button class = "nav-button" onclick="chooseOption('team-task')">Wyświetl zadania zespołu</button>
                <button class = "nav-button" onclick="chooseOption('team')">Zarządzaj zespołem</button>`
                else if (position == "sectionManager")
                    nav.innerHTML = `<button class = "nav-button" onclick="chooseOption('main')">Główna strona</button>
                <button class = "nav-button" onclick="chooseOption('data')">Wyświetl dane użytkownika</button>
                <button class = "nav-button" onclick="chooseOption('task')">Wyświetl swoje zadania</button>
                <button class = "nav-button" onclick="chooseOption('section-task')">Wyświetl zadania sekcji</button>
                <button class = "nav-button" onclick="chooseOption('section')">Zarządzaj sekcją</button>`
                else if (position == "studioHead")
                    nav.innerHTML = `<button class = "nav-button" onclick="chooseOption('main')">Główna strona</button>
                <button class = "nav-button" onclick="chooseOption('data')">Wyświetl dane użytkownika</button>
                <button class = "nav-button" onclick="chooseOption('task')">Wyświetl swoje zadania</button>
                <button class = "nav-button" onclick="chooseOption('employees')">Zarządzaj pracownikami</button>
                <button class = "nav-button" onclick="chooseOption('sections')">Zarządzaj sekcjami</button>`
                }

                async function chooseOpt(type,position) {
                    if (type == 'main')
                    {
                        if (position == "employee")
                        location.href =`/employee`;
                        else if (position == "teamManager")
                        location.href =`/team-manager`;
                        else if (position == "sectionManager")
                        location.href =`/section-manager`;
                        else if (position == "studioHead")
                        location.href =`/chief`;
                    }

                    if (type == 'data')
                    {
                        location.href =`/your-data`;  
                    }
                    if (type == 'task')
                    {
                      location.href =`/your-tasks`;  
                    }
                    if (type == 'employee-task')
                    {
                        location.href =`/team-employees/tasks`;   
                    }
                    if (type == 'team-task')
                    {
                        location.href =`/team-tasks`;  
                    }
                    if (type == 'team')
                    {   
                        location.href =`/team-employees`; 
                    }
                    if (type == 'section-task')
                    {                        
                        location.href =`/section-tasks`;  
                    }
                    if (type == 'section')
                    {                        
                        location.href =`/section-teams`;  
                    }
                    if (type == 'employees')
                    {
                      location.href =`/all-employees`;  
                    }
                    if (type == 'sections')
                    {
                        location.href =`/sections`;  
                    }
                    if (type == 'logout')
                    {
                        clearSession();
                        location.replace("/");  
                    }
                }
                async function saveSingleValue(key, value) {
                try {
                    const response = await fetch('/api/session/set', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({ [key]: value })
                    });
                    return await response.json();
                } catch (error) {
                    console.error('Błąd zapisu:', error);
                    return null;
                }
                }
                async function clearSession() {
                if (!confirm('Czy na pewno chcesz się wylogować? Tej operacji nie można cofnąć.')) {
                    return;
                }
                try {
                    const response = await fetch('/api/session/clear', {
                        method: 'POST'
                    });
                    const result = await response.json();
                } catch (error) {
                    statusDiv.className = 'status error';
                    statusDiv.textContent = `Błąd: ${error.message}`;
                }
            }