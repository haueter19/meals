// Submits form for new meal
document.getElementById('submit-btn').addEventListener('click', function() {
    const jsonData = {
        name: document.getElementById('name').value,
        description: document.getElementById('description').value,
        cuisine_type: document.getElementById('cuisine_type').value,
        cooking_mode: document.getElementById('cooking_mode').value,
        cooking_ease: document.getElementById('cooking_ease').value,
        cooking_time: document.getElementById('cooking_time').value,
        image_path: document.getElementById('image_path').value,
        source_url: document.getElementById('source_url').value,
        ingredients: [],
        directions: [],
        log_entries: [],
    };

    ingredientRows = document.querySelectorAll('.ingredient-row');
    ingredientRows.forEach(row => {
        const ingredientName = row.querySelector(`input[name^="ingredient_"][name$="_name"]`).value;
        const ingredientQuantity = row.querySelector(`input[name^="ingredient_"][name$="_quantity"]`).value;
        const ingredientUnit = row.querySelector(`input[name^="ingredient_"][name$="_unit"]`).value;
        if (ingredientName) {
            jsonData.ingredients.push({
                name: ingredientName,
                quantity: ingredientQuantity,
                unit: ingredientUnit
            });
        }
    });

    let stepNumber = 0;
    document.querySelectorAll('.directions-row').forEach(item => {
        if (item.querySelector('input[name^="direction_"]').value != ''){
            stepNumber++;
            jsonData.directions.push({
                step_number: stepNumber,
                description: item.querySelector('input[name^="direction_"]').value
            });
        }     
    });

    //let logEntryNum = 0;
    document.querySelectorAll('.log-row').forEach(item => {
        const logEntryDate = item.querySelector(`input[name^="log_entry_date_"]`).value;
        const logEntryRating = item.querySelector(`input[name^="log_entry_rating_"]`).value;
        const logEntryNotes = item.querySelector(`input[name^="log_entry_notes_"]`).value;
        if (logEntryDate != ''){
            //logEntryNum++;
            jsonData.log_entries.push({
                date: logEntryDate,
                rating: -1,
                notes: logEntryNotes
            });
        }     
    });

    console.log(jsonData)

    if (mealData.meal_id >= 0){
        method = 'PUT'
        url = `/meals/${mealData.meal_id}`
        body = JSON.stringify(jsonData)
    } else {
        method = 'POST'
        url = '/meals/'
        body = JSON.stringify(jsonData)
    }
    
    fetch(url, {
        method: method,
        headers: {
            'Content-Type': 'application/json'
        },
        body: body
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        // Assuming success, now upload the image
        
        uploadImage();
        alert('This meal has been saved')
        window.location = window.location.host+"/find"
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});

function addIngredient() {
    const container = document.getElementById('ingredientContainer');
    const newRow = document.createElement('div');
    newRow.className = 'ingredient-row mb-1';
    let i = container.childElementCount + 1;
    newRow.innerHTML = `
        <input type="text" name="ingredient_${i}_name" class="ingredient-name" placeholder="Ingredient name">
        <input type="number" name="ingredient_${i}_quantity" class="ingredient-quantity" placeholder="Quantity" style="max-width:100px">
        <input type="text" name="ingredient_${i}_unit" class="ingredient-unit" placeholder="Unit (e.g., cups, pieces)">
        <button type="button" class="btn btn-sm delete-btn btn-danger" onclick="this.parentElement.remove()">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash3" viewBox="0 0 16 16">
                <path d="M6.5 1h3a.5.5 0 0 1 .5.5v1H6v-1a.5.5 0 0 1 .5-.5M11 2.5v-1A1.5 1.5 0 0 0 9.5 0h-3A1.5 1.5 0 0 0 5 1.5v1H1.5a.5.5 0 0 0 0 1h.538l.853 10.66A2 2 0 0 0 4.885 16h6.23a2 2 0 0 0 1.994-1.84l.853-10.66h.538a.5.5 0 0 0 0-1zm1.958 1-.846 10.58a1 1 0 0 1-.997.92h-6.23a1 1 0 0 1-.997-.92L3.042 3.5zm-7.487 1a.5.5 0 0 1 .528.47l.5 8.5a.5.5 0 0 1-.998.06L5 5.03a.5.5 0 0 1 .47-.53Zm5.058 0a.5.5 0 0 1 .47.53l-.5 8.5a.5.5 0 1 1-.998-.06l.5-8.5a.5.5 0 0 1 .528-.47M8 4.5a.5.5 0 0 1 .5.5v8.5a.5.5 0 0 1-1 0V5a.5.5 0 0 1 .5-.5"/>
            </svg>
        </button>
    `;
    container.appendChild(newRow);
}

function addDirection() {
    const container = document.getElementById('directionContainer');
    const newRow = document.createElement('div');
    let j = container.childElementCount + 1
    newRow.className = 'directions-row mb-1 w-100';
    newRow.innerHTML = `
        <input type="text" class="w-75" name="direction_${j}" placeholder="Step ${j} Description" style="min-width:250px;">
        <button type="button" class="btn btn-sm delete-btn btn-danger" onclick="this.parentElement.remove()">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash3" viewBox="0 0 16 16">
                <path d="M6.5 1h3a.5.5 0 0 1 .5.5v1H6v-1a.5.5 0 0 1 .5-.5M11 2.5v-1A1.5 1.5 0 0 0 9.5 0h-3A1.5 1.5 0 0 0 5 1.5v1H1.5a.5.5 0 0 0 0 1h.538l.853 10.66A2 2 0 0 0 4.885 16h6.23a2 2 0 0 0 1.994-1.84l.853-10.66h.538a.5.5 0 0 0 0-1zm1.958 1-.846 10.58a1 1 0 0 1-.997.92h-6.23a1 1 0 0 1-.997-.92L3.042 3.5zm-7.487 1a.5.5 0 0 1 .528.47l.5 8.5a.5.5 0 0 1-.998.06L5 5.03a.5.5 0 0 1 .47-.53Zm5.058 0a.5.5 0 0 1 .47.53l-.5 8.5a.5.5 0 1 1-.998-.06l.5-8.5a.5.5 0 0 1 .528-.47M8 4.5a.5.5 0 0 1 .5.5v8.5a.5.5 0 0 1-1 0V5a.5.5 0 0 1 .5-.5"/>
            </svg>
        </button>
    `;
    container.appendChild(newRow);
}


function addMealLogEntry() {
    const container = document.getElementById('mealLogContainer');
    const newRow = document.createElement('div');
    newRow.className = 'log-row mb-1 w-100';
    let i = container.childElementCount + 1;
    newRow.innerHTML = `
        <input type="date" name="log_entry_date_${i}" class="log-date" placeholder="Date">
        <input type="number" name="log_entry_rating_${i}" class="log-rating" size="4" min=0 max=10 placeholder="Rating">
        <input type="text" name="log_entry_notes_${i}" class="log-notes" size="80" placeholder="Notes">
        <button type="button" class="btn btn-sm delete-btn btn-danger" onclick="this.parentElement.remove()">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash3" viewBox="0 0 16 16">
                <path d="M6.5 1h3a.5.5 0 0 1 .5.5v1H6v-1a.5.5 0 0 1 .5-.5M11 2.5v-1A1.5 1.5 0 0 0 9.5 0h-3A1.5 1.5 0 0 0 5 1.5v1H1.5a.5.5 0 0 0 0 1h.538l.853 10.66A2 2 0 0 0 4.885 16h6.23a2 2 0 0 0 1.994-1.84l.853-10.66h.538a.5.5 0 0 0 0-1zm1.958 1-.846 10.58a1 1 0 0 1-.997.92h-6.23a1 1 0 0 1-.997-.92L3.042 3.5zm-7.487 1a.5.5 0 0 1 .528.47l.5 8.5a.5.5 0 0 1-.998.06L5 5.03a.5.5 0 0 1 .47-.53Zm5.058 0a.5.5 0 0 1 .47.53l-.5 8.5a.5.5 0 1 1-.998-.06l.5-8.5a.5.5 0 0 1 .528-.47M8 4.5a.5.5 0 0 1 .5.5v8.5a.5.5 0 0 1-1 0V5a.5.5 0 0 1 .5-.5"/>
            </svg>
        </button>
    `;
    container.appendChild(newRow);
}

function uploadImage() {
    const form = document.getElementById('uploadForm');
    if (!form) {
        console.error('Form element not found');
        return;
    }
    //const mealId = document.getElementById('meal_id').value;
    if (!mealData['meal_id']) {
        console.error('Meal ID is required');
        return;
    }

    const imageInput = document.getElementById('image_uploader');
    if (!imageInput.files.length) {  // Check if an image is selected
        console.log('No image selected by user');
        return;
    }

    const formData = new FormData(form);
    console.log('made it here', formData)
    fetch(`/meals/${mealData['meal_id']}/upload-image/`, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

async function deleteMeal(meal_id){
    const confirmation = confirm('Are you sure you want to delete this meal?');

    if (confirmation){
        try {
            const response = await fetch(`/meals/${meal_id}`, {
                method: 'DELETE',
            });
            if (!response.ok) throw new Error('Failed to delete meal');
            /*
            document.getElementById(`meal_${meal_id}`).innerHTML = `
                    <div id="meal_${meal_id}" class="card shadow-med">
                        <div class="card-body">
                            <p class="card-text">This meal has been deleted</p>
                        </div>
                    </div>`;
            */
            console.log(`Successfully deleted meal with id: ${meal_id}`)
            window.location = window.location.origin+'/find'
        } catch (error) {
            console.error(error);
            alert("Error deleting meals. Please try again later.");
        }
    } else {
        console.log('Delete cancelled')
    }   
}

$(document).ready(function(){
    // Adds any existing ingredients
    ingredient_num = 0;
    $.each(mealData['ingredients'], function(k,v){
        ingredient_num++;
        addIngredient();
        $('input[name="ingredient_'+ingredient_num+'_name"]').val(v['name']);
        $('input[name="ingredient_'+ingredient_num+'_quantity"]').val(v['quantity']);
        $('input[name="ingredient_'+ingredient_num+'_unit"]').val(v['unit']);
    })

    // Adds any existing directions
    direction_step = 0;
    $.each(mealData['directions'], function(k,v){
        direction_step++;
        addDirection()
        $('input[name="direction_'+direction_step+'"]').val(v['description']);
    })

    // Adds any existing log entries
    let log_entry_num = 0;
    $.each(mealData['logEntries'], function(k,v){
        log_entry_num++;
        addMealLogEntry()
        $('input[name="log_entry_date_'+log_entry_num+'"]').val(v['date']);
        $('input[name="log_entry_rating_'+log_entry_num+'"]').val(v['rating']);
        $('input[name="log_entry_notes_'+log_entry_num+'"]').val(v['notes']);
    })

    let mealStatsHtml = '';
    $.each(mealData['mealStats'], function(k,v){
        mealStatsHtml += `${k}: ${v}<br>`;
    })
    $("#mealStatsContainer").html(mealStatsHtml)


    document.getElementById('image_uploader').addEventListener('change', function(event) {
        const fileName = event.target.files[0]?.name; // Get the selected file name
        if (fileName) {
            console.log("Selected file:", fileName);
            $("#image_path").val(fileName)
        } else {
            $("#image_path").val('Bad file selection. Try again')
        }
    });
    

  });