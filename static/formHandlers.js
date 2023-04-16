function createProject(event) {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);

    for (const [name, value] of formData) {
        console.log(`${name}: ${value}`)
    }

    fetch('/project', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(Object.fromEntries(formData))
    })
    .then(response => {
    // Handle the response as needed
        console.log(response)
    })
    .catch(error => {
    // Handle the error as needed
    });
    return false;
}


function getProjectDetails() {
    const projectId = document.getElementById("project_id").value;
    fetch(`/project?project_id=${projectId}`, {
      method: "GET",
    })
      .then((response) => response.json())
      .then((project) => {
        const projectDetails = document.getElementById("project_details");
        projectDetails.innerHTML = `
          <h2>${project.name}</h2>
          <p>${project.description}</p>
          <p>${project.pm_email}</p>
          <p>${project.date_created}</p>
          <p>${project.status}</p>
          <p>${project.date_completed}</p>
        `;
      })
      .catch((error) => {
        console.error("Error fetching project details:", error);
        const projectDetails = document.getElementById("project_details");
        projectDetails.innerHTML = `
          <p>Project not found.</p>
        `;
      });
    }