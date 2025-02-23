function viewMeal(meal_id){
    window.location = window.location.origin+'/meal/'+meal_id
}


document.addEventListener("DOMContentLoaded", () => {
    const mealList = document.getElementById("meal-list");
    const nextBtn = document.getElementById("next-btn");
    let skip = 0;
    const limit = 10;

    

    async function fetchMeals() {
        try {
            const response = await fetch(`/meals/?skip=${skip}&limit=${limit}`);
            if (!response.ok) throw new Error("Failed to fetch meals");

            const meals = await response.json();
            if (meals.length === 0) {
                nextBtn.disabled = true;
                nextBtn.textContent = "No more meals";
                return;
            }

            meals.forEach(meal => {
                console.log(meal)
                
                if (meal.meal_stats.length>0){
                    meal_count = meal.meal_stats[0]['meal_count']
                    recent_meal_date = meal.meal_stats[0]['recent_meal_date']
                } else {
                    meal_count = 0
                    recent_meal_date = 'Never eaten'
                }
                const mealCard = document.createElement("div");
                mealCard.className = "col-md-6 col-lg-4 mb-3 d-flex align-items-stretch";
                //<div class="col-lg-4 mb-3 d-flex align-items-stretch"></div>
                
                mealCard.innerHTML = `
                    <div id="meal_${meal.meal_id}" class="card shadow-med">

                        <img src="/assets/images/${meal.image_path}" || '/assets/images/image.jpg'}" class="card-img-top" max-height="275" style="object-fit: contain;">
                        <div class="card-body">
                            <h5 class="card-title">${meal.name}</h5>
                            <p class="card-text">${meal.description || "No description available."}</p>
                            <p>Meal count: <span class="badge bg-secondary">${meal_count}</span></p>
                            <p>Most recent meal: ${recent_meal_date}</p>
                            
                            <div class="btn-toolbar" role="group" aria-label="Basic outlined example">
                                <a href="/meal/${meal.meal_id}" class="btn btn-outline-primary mx-2 stretched-link">View</a>
                            </div>
                            <br>
                            <span class="badge bg-info mt-2">${meal.cuisine_type}</span>
                            <span class="badge bg-primary mt-2">${meal.cooking_mode}</span>
                            <span class="badge bg-warning mt-2">${meal.cooking_ease}</span>
                        </div>
                    </div>
                `;
                mealList.appendChild(mealCard);
            });

            skip += limit;
        } catch (error) {
            console.error(error);
            alert("Error fetching meals. Please try again later.");
        }
    }

    nextBtn.addEventListener("click", fetchMeals);
    fetchMeals(); // Load initial meals on page load

    
});
