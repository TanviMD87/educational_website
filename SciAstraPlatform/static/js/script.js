// Fetch discounted courses and display them on the homepage
document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/discounted_courses')
        .then(response => response.json())
        .then(data => {
            let coursesContainer = document.getElementById('courses-list');
            data.forEach(course => {
                let courseElement = `
                    <div class="col-md-4 mb-4">
                        <div class="card course-card">
                            <img src="${course.image_url}" class="card-img-top" alt="${course.name}">
                            <div class="card-body">
                                <h5 class="card-title">${course.name}</h5>
                                <p class="card-text">${course.description}</p>
                                <p class="text-muted">Discounted Price: $${course.price}</p>
                                <a href="/courses/${course.id}" class="btn btn-primary">View Details</a>
                            </div>
                        </div>
                    </div>
                `;
                coursesContainer.innerHTML += courseElement;
            });
        })
        .catch(error => console.error('Error fetching courses:', error));
});
