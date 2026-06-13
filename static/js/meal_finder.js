function viewMeal(meal_id){
    window.location = window.location.origin+'/meal/'+meal_id
}

function isUrl(str) {
    return str && (str.startsWith('http://') || str.startsWith('https://'));
}

function formatDate(dateStr) {
    if (!dateStr || dateStr === 'Never eaten') return dateStr;
    const parts = dateStr.split('-');
    if (parts.length === 3) return `${parts[1]}/${parts[2]}/${parts[0]}`;
    return dateStr;
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

            const imgSrc = meal.image_path ? `/assets/images/${meal.image_path}` : '/assets/images/image.jpg';
            mealCard.innerHTML = `
                <div id="meal_${meal.meal_id}" class="meal-card w-100">
                    <div class="card-img-wrap">
                        <img src="${imgSrc}" alt="${meal.name}" onerror="this.src='/assets/images/image.jpg'">
                    </div>
                    <div class="card-body">
                        <h5 class="card-title">${meal.name}</h5>
                        <p class="card-desc">${meal.description || "No description available."}</p>
                        <div class="tag-row">
                            ${meal.cuisine_type ? `<span class="tag tag-cuisine">${meal.cuisine_type}</span>` : ''}
                            ${meal.cooking_mode  ? `<span class="tag tag-mode">${meal.cooking_mode}</span>`   : ''}
                            ${meal.cooking_ease  ? `<span class="tag tag-ease">${meal.cooking_ease}</span>`   : ''}
                        </div>
                        <div class="card-footer-inner">
                            <div>
                                <div class="stat-item">Times made: <strong>${meal_count}</strong></div>
                                <div class="stat-item">Last eaten: <strong>${formatDate(recent_meal_date)}</strong></div>
                            </div>
                            <div class="action-row">
                                <a href="/meal/${meal.meal_id}" class="btn-view">View</a>
                                ${meal.source_url && isUrl(meal.source_url) ? `<a href="${meal.source_url}" target="_blank" rel="noopener noreferrer" class="btn-source">Source</a>` : ''}
                            </div>
                        </div>
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
