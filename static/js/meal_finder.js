function viewMeal(meal_id){
    window.location = window.location.origin+'/meal/'+meal_id
}


document.addEventListener("DOMContentLoaded", () => {
    const mealList = document.getElementById("meal-list");
    const nextBtn = document.getElementById("next-btn");
    const searchInput = document.getElementById("filter-search");
    const cuisineSelect = document.getElementById("filter-cuisine");
    const modeSelect = document.getElementById("filter-mode");
    const easeSelect = document.getElementById("filter-ease");
    const clearBtn = document.getElementById("clear-filters-btn");

    let skip = 0;
    const limit = 102;
    let allMeals = [];

    function renderMeals(meals) {
        mealList.innerHTML = "";
        meals.forEach(meal => {
            let meal_count, recent_meal_date;
            if (meal.meal_stats.length > 0) {
                meal_count = meal.meal_stats[0]['meal_count'];
                recent_meal_date = meal.meal_stats[0]['recent_meal_date'];
            } else {
                meal_count = 0;
                recent_meal_date = 'Never eaten';
            }

            const mealCard = document.createElement("div");
            mealCard.className = "col-md-6 col-lg-4 mb-3 d-flex align-items-stretch";

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
    }

    function filterMeals() {
        const searchTerm = searchInput.value.toLowerCase();
        const cuisine = cuisineSelect.value;
        const mode = modeSelect.value;
        const ease = easeSelect.value;

        const filtered = allMeals.filter(meal => {
            if (searchTerm) {
                const name = (meal.name || "").toLowerCase();
                const desc = (meal.description || "").toLowerCase();
                if (!name.includes(searchTerm) && !desc.includes(searchTerm)) return false;
            }
            if (cuisine && meal.cuisine_type !== cuisine) return false;
            if (mode && meal.cooking_mode !== mode) return false;
            if (ease && meal.cooking_ease !== ease) return false;
            return true;
        });

        renderMeals(filtered);
    }

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

            allMeals = allMeals.concat(meals);
            filterMeals();
            skip += limit;
        } catch (error) {
            console.error(error);
            alert("Error fetching meals. Please try again later.");
        }
    }

    searchInput.addEventListener("input", filterMeals);
    cuisineSelect.addEventListener("change", filterMeals);
    modeSelect.addEventListener("change", filterMeals);
    easeSelect.addEventListener("change", filterMeals);

    clearBtn.addEventListener("click", () => {
        searchInput.value = "";
        cuisineSelect.value = "";
        modeSelect.value = "";
        easeSelect.value = "";
        renderMeals(allMeals);
    });

    nextBtn.addEventListener("click", fetchMeals);
    fetchMeals();
});
