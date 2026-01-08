        const API_BASE_URL = 'http://localhost:8000';
        let currentRecipes = [];
        let allCategories = new Set();


        document.addEventListener('DOMContentLoaded', () => {
            loadAllRecipes();
            resetFormToAddMode(); // מבטיח שהטופס מתחיל במצב הוספה
        });


        function switchTab(tabName) {
            // 1. הסרת מחלקת active מכל התוכן ומכל הכפתורים
            document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));


            // 2. הצגת הטאב המבוקש
            const targetTab = document.getElementById(tabName);
            if (targetTab) {
                targetTab.classList.add('active');
            }


            // 3. סימון הכפתור הנכון כפעיל
            if (window.event && window.event.target && window.event.target.classList.contains('tab-btn')) {
                // אם הלחיצה באה ישירות מכפתור ב-HTML
                window.event.target.classList.add('active');
            } else {
                // אם הקריאה באה מתוך קוד (כמו editRecipe), נחפש את הכפתור המתאים לפי הטקסט או המיקום
                const buttons = document.querySelectorAll('.tab-btn');
                buttons.forEach(btn => {
                    // התאמה לפי הלוגיקה של הטאבים שלך
                    if (tabName === 'all-recipes' && btn.textContent.includes('כל המתכונים')) btn.classList.add('active');
                    if (tabName === 'add-recipe' && btn.textContent.includes('הוסיפו מתכון')) btn.classList.add('active');
                    if (tabName === 'ai-assistant' && btn.textContent.includes('עוזר חכם')) btn.classList.add('active');
                });
            }


            // 4. אם עוברים לטאב אחר (לא עריכה), מחזירים את הטופס למצב הוספה
            if (tabName !== 'add-recipe') {
                resetFormToAddMode();
            }
        }


        function resetFormToAddMode() {
            const form = document.getElementById('add-recipe-form');
            if (form) {
                form.reset();
                const titleElement = form.querySelector('.form-title');
                const submitBtn = form.querySelector('button[type="submit"]');
               
                if (titleElement) {
                    titleElement.textContent = 'מתכון חדש ומיוחד';
                }
                if (submitBtn) {
                    submitBtn.textContent = 'הוסיפו מתכון ✨';
                }
               
                // מחזירים את הפעולה המקורית של הטופס
                form.onsubmit = async (e) => {
                    e.preventDefault();
                    await addRecipe();
                };
            }
        }


        async function loadAllRecipes() {
            try {
                const response = await fetch(`${API_BASE_URL}/recipes`);
                if (!response.ok) throw new Error('שגיאה בטעינה');
                const recipes = await response.json();
                currentRecipes = recipes;
                recipes.forEach(recipe => { if (recipe.category) allCategories.add(recipe.category); });
                displayRecipes(recipes, 'recipes-container');
            } catch (error) {
                document.getElementById('recipes-container').innerHTML = `
                    <div class="empty-state">
                        <div class="empty-state-icon">⚠️</div>
                        <h2 class="empty-state-title">אופס!</h2>
                        <p class="empty-state-text">${error.message}</p>
                        <button class="btn btn-primary" onclick="loadAllRecipes()" style="margin-top: 2rem;">נסו שוב</button>
                    </div>
                `;
            }
        }


        function displayRecipes(recipes, containerId) {
            const container = document.getElementById(containerId);
            if (recipes.length === 0) {
                container.innerHTML = `
                    <div class="empty-state">
                        <div class="empty-state-icon">🍽️</div>
                        <h2 class="empty-state-title">אין מתכונים</h2>
                        <p class="empty-state-text">עדיין אין מתכונים להצגה</p>
                    </div>
                `;
                return;
            }
            container.innerHTML = recipes.map(recipe => `
                <div class="recipe-card" onclick="viewRecipe(${recipe.id})">
                    <div class="recipe-image-wrapper">
                        ${recipe.image_url ?
                    `<img src="${recipe.image_url}" alt="${recipe.name}" class="recipe-image" onerror="this.parentElement.style.background='linear-gradient(135deg, #FFCCBC 0%, #B2DFDB 100%)'">` :
                    `<div style="height: 280px; display: flex; align-items: center; justify-content: center; font-size: 5rem;">🍴</div>`
                }
                        <span class="recipe-badge">${recipe.category || 'כללי'}</span>
                    </div>
                    <div class="recipe-content">
                        <h3 class="recipe-title">${recipe.name}</h3>
                        <p class="recipe-description">${recipe.description || 'מתכון טעים ומיוחד'}</p>
                        <div class="recipe-meta">
                            ${recipe.prep_time ? `<span>⏱️ ${recipe.prep_time} דקות</span>` : ''}
                            ${recipe.servings ? `<span>👥 ${recipe.servings} מנות</span>` : ''}
                        </div>
                        <div class="recipe-actions">
                            <button class="btn btn-primary" onclick="event.stopPropagation(); viewRecipe(${recipe.id})">צפו במתכון</button>
                            <button class="btn btn-secondary" onclick="event.stopPropagation(); editRecipe(${recipe.id})">ערכו</button>
                            <button class="btn btn-danger" onclick="event.stopPropagation(); deleteRecipe(${recipe.id})">מחקו</button>
                        </div>
                    </div>
                </div>
            `).join('');
        }






        async function viewRecipe(id) {
            try {
                const response = await fetch(`${API_BASE_URL}/recipes/${id}`);
                if (!response.ok) throw new Error('שגיאה');
                const recipe = await response.json();
                const ingredientsList = Array.isArray(recipe.ingredients) ?
                    recipe.ingredients.map(ing => `<li>${ing}</li>`).join('') :
                    recipe.ingredients ? `<li>${recipe.ingredients}</li>` : '';
                document.getElementById('recipe-detail-content').innerHTML = `
                    <div class="recipe-detail">
                        <div class="recipe-detail-header">
                            <span class="recipe-detail-category">${recipe.category || 'כללי'}</span>
                            <h2 class="recipe-detail-title">${recipe.name}</h2>
                        </div>
                        ${recipe.image_url ? `<img src="${recipe.image_url}" alt="${recipe.name}" class="recipe-detail-image">` : ''}
                        ${recipe.description ? `<div class="recipe-detail-section"><p>${recipe.description}</p></div>` : ''}
                        <div class="recipe-detail-section"><h3>מצרכים</h3><ul>${ingredientsList}</ul></div>
                        <div class="recipe-detail-section"><h3>הוראות הכנה</h3><p>${recipe.instructions || ''}</p></div>
                        ${recipe.prep_time || recipe.servings ? `<div class="recipe-meta" style="justify-content: center; border: none;">
                            ${recipe.prep_time ? `<span>⏱️ ${recipe.prep_time} דקות</span>` : ''}
                            ${recipe.servings ? `<span>👥 ${recipe.servings} מנות</span>` : ''}
                        </div>` : ''}
                    </div>
                `;
                document.getElementById('recipe-modal').classList.add('active');
            } catch (error) { alert('שגיאה: ' + error.message); }
        }


        function closeModal() { document.getElementById('recipe-modal').classList.remove('active'); }


        async function addRecipe() {
            const form = document.getElementById('add-recipe-form');
            const formData = new FormData(form);
            const recipe = {
                name: formData.get('name'),
                category: formData.get('category_id'), // חזרה ל-category
                description: formData.get('description') || "", // מבטיח שתמיד תשלח מחרוזת, גם אם ריקה
                ingredients: formData.get('ingredients').split('\n').filter(i => i.trim()),
                instructions: formData.get('instructions'),
                prep_time_minutes: parseInt(formData.get('prep_time')) || 0,
                servings: parseInt(formData.get('servings')) || 0,
                image_url: formData.get('image_url') || ""
            };
            try {
                const response = await fetch(`${API_BASE_URL}/recipes`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(recipe)
                });
                if (!response.ok) throw new Error('שגיאה');
                alert('המתכון נוסף בהצלחה! ✨');
                form.reset();
                await loadAllRecipes();
                switchTab('all-recipes');
            } catch (error) { alert('שגיאה: ' + error.message); }
        }


async function editRecipe(id) {
    try {
        const response = await fetch(`${API_BASE_URL}/recipes/${id}`);
       
        if (!response.ok) {
            throw new Error(`שגיאה ${response.status}: ${response.statusText}`);
        }
       
        const recipe = await response.json();
        console.log('Recipe data:', recipe); // לבדיקה


        // 1. עוברים לטאב של הטופס
        switchTab('add-recipe');
       
        const form = document.getElementById('add-recipe-form');
        const submitBtn = form.querySelector('button[type="submit"]');


        // 2. ממלאים את הנתונים בטופס
        form.elements.name.value = recipe.name || '';
       
        // ממירים category_id לשם קטגוריה
        const categoryMap = { 1: 'קינוחים', 2: 'עוגות', 3: 'עוגיות', 4: 'בריא' };
        form.elements.category_id.value = categoryMap[recipe.category_id] || '';
       
        form.elements.description.value = recipe.description || '';
        form.elements.ingredients.value = Array.isArray(recipe.ingredients) ? recipe.ingredients.join('\n') : (recipe.ingredients || '');
        form.elements.instructions.value = recipe.instructions || '';
        form.elements.prep_time.value = recipe.prep_time_minutes || recipe.prep_time || '';
        form.elements.servings.value = recipe.servings || '';
        form.elements.image_url.value = recipe.image_url || '';


        // 3. שינוי כותרת וכפתור
        const titleElement = form.querySelector('.form-title');
        if (titleElement) {
            titleElement.textContent = 'עריכת מתכון: ' + (recipe.name || 'ללא שם');
        }
        if (submitBtn) {
            submitBtn.textContent = 'שמור שינויים 💾';
        }


        // 4. שינוי האירוע של הטופס
        form.onsubmit = async (e) => {
            e.preventDefault();
            await testUpdateRecipe(id);
        };


        window.scrollTo({ top: 0, behavior: 'smooth' });


    } catch (error) {
        console.error('Edit recipe error:', error);
        alert('שגיאה בטעינת הנתונים לעריכה: ' + error.message);
    }
}
 async function testUpdateRecipe(id) {
    try {
        // 1. איסוף הנתונים מהטופס (באמצעות ה-ID של הטופס הקיים ב-HTML שלך)
        const form = document.getElementById('add-recipe-form');
        const formData = new FormData(form);


        const updatedData = {
            name: formData.get('name'),
            description: formData.get('description'),
            // הפיכת טקסט המצרכים למערך (מפריד לפי שורות)
            ingredients: formData.get('ingredients').split('\n').filter(i => i.trim()),
            instructions: formData.get('instructions'),
            prep_time_minutes: parseInt(formData.get('prep_time')) || 0,
            servings: parseInt(formData.get('servings')) || 0,
            category: formData.get('category_id'),
            image_url: formData.get('image_url') || ""
        };


        // 2. כאן נכנס הקוד ששאלת עליו - השליחה לשרת:
        const response = await fetch(`${API_BASE_URL}/recipes/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(updatedData)
        });


        if (!response.ok) {
            throw new Error('שגיאה בעדכון המתכון מול השרת');
        }


        // 3. הצלחה ורענון הדף
        alert("השינויים נשמרו בהצלחה! 🎉");
        resetFormToAddMode(); // מחזיר את הטופס למצב "הוספה"
        await loadAllRecipes(); // טוען מחדש את רשימת המתכונים המעודכנת
        switchTab('all-recipes'); // מחזיר את המשתמש לתצוגת כל המתכונים


    } catch (error) {
        console.error('Error:', error);
        alert("חלה שגיאה: " + error.message);
    }
}




async function sendChatMessage() {
    const input = document.getElementById('chat-input');
    const message = input.value.trim();
    if (!message) return;


    const chatMessages = document.getElementById('chat-messages');
   
    // הצגת הודעת המשתמש
    chatMessages.innerHTML += `<div class="chat-message user"><strong>השאלה שלכם</strong><p>${message}</p></div>`;
    input.value = '';
   
    // הוספת הודעת "חושב..." זמנית
    const loadingId = 'loading-' + Date.now();
    chatMessages.innerHTML += `<div class="chat-message ai" id="${loadingId}"><strong>העוזר החכם</strong><p>מתכננת תשובה מתוקה... 🧁</p></div>`;
   
    chatMessages.scrollTop = chatMessages.scrollHeight;


    try {
        const response = await fetch(`${API_BASE_URL}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question: message })
        });
       
        if (!response.ok) throw new Error('שגיאה');
        const data = await response.json();
       
        // החלפת הודעת הטעינה בתשובה האמיתית
        document.getElementById(loadingId).querySelector('p').innerText = data.answer;
       
    } catch (error) {
        document.getElementById(loadingId).querySelector('p').innerText = "מצטערת, אירעה שגיאה בחיבור לבוט. בדקו שהשרת מופעל. 😔";
    }
    chatMessages.scrollTop = chatMessages.scrollHeight;
}


        async function chooseCategory(categoryName) {
            try {
                const response = await fetch(`${API_BASE_URL}/recipes/category/${categoryName}`);


                if (!response.ok) {
                    throw new Error('שגיאה בתקשורת עם השרת');
                }


                const filteredRecipes = await response.json();


                // מעבר לטאב קטגוריות קודם
                switchTab('categories');


                // אם הרשימה ריקה
                if (filteredRecipes.length === 0) {
                    document.getElementById('category-recipes-container').innerHTML = `
                <div class="empty-state">
                    <p>עדיין אין מתכונים בקטגוריית ${categoryName} 🥣</p>
                </div>`;
                    return;
                }


                // הצגת המתכונים
                displayRecipes(filteredRecipes, 'category-recipes-container');


            } catch (error) {
                console.error("Error:", error);
                alert('שגיאה בטעינת מתכוני הקטגוריה');
            }
        }


async function deleteRecipe(id) {
    // הצגת הודעת אישור למשתמש
    const confirmed = confirm("האם אתם בטוחים שברצונכם למחוק את המתכון הזה?");
   
    if (!confirmed) return; // אם המשתמש התחרט, לא עושים כלום


    try {
        const response = await fetch(`${API_BASE_URL}/recipes/${id}`, {
            method: 'DELETE',
        });


        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'שגיאה במחיקה');
        }


        alert('המתכון נמחק בהצלחה! 🗑️');
       
        // רענון הרשימה כדי שהמתכון ייעלם מהמסך
        await loadAllRecipes();
       
    } catch (error) {
        console.error("Error deleting recipe:", error);
        alert("אופס! " + error.message);
    }
}




