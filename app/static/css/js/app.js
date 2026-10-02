async function apiRequest(url, options = {}) {
    const response = await fetch(url, {
        credentials: "include",
        ...options
    });

    let data = {};

    try {
        data = await response.json();
    } catch (error) {
        data = {};
    }

    if (!response.ok) {
        throw new Error(
            data.detail || "Something went wrong."
        );
    }

    return data;
}


/* -------------------------------
   SESSION
-------------------------------- */

async function loadSession() {

    try {

        const data = await apiRequest(
            "/auth/session-info"
        );

        const loginLink =
            document.getElementById("loginLink");

        const registerLink =
            document.getElementById("registerLink");

        const dashboardLink =
            document.getElementById("dashboardLink");

        const logoutForm =
            document.getElementById("logoutForm");

        if (data.authenticated) {

            if (loginLink) {
                loginLink.classList.add("hidden");
            }

            if (registerLink) {
                registerLink.classList.add("hidden");
            }

            if (dashboardLink) {
                dashboardLink.classList.remove("hidden");
            }

            if (logoutForm) {
                logoutForm.classList.remove("hidden");
            }

            const username =
                document.getElementById("username");

            if (username) {
                username.textContent =
                    data.user.username;
            }

        } else {

            if (dashboardLink) {
                dashboardLink.classList.add("hidden");
            }

            if (logoutForm) {
                logoutForm.classList.add("hidden");
            }
        }

    } catch (error) {
        console.error(error);
    }
}


/* -------------------------------
   LOGOUT
-------------------------------- */

async function logout(event) {

    if (event) {
        event.preventDefault();
    }

    try {

        await apiRequest(
            "/auth/logout",
            {
                method: "POST"
            }
        );

        window.location.href = "/";

    } catch (error) {

        alert(error.message);
    }
}


/* -------------------------------
   LOGIN
-------------------------------- */

async function loginUser(event) {

    event.preventDefault();

    const form =
        document.getElementById("loginForm");

    const message =
        document.getElementById("formMessage");

    const email =
        document.getElementById("email").value;

    const password =
        document.getElementById("password").value;

    try {

        const data = await apiRequest(
            "/auth/login",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    email: email,
                    password: password
                })
            }
        );

        message.className =
            "alert alert-success";

        message.textContent =
            data.message;

        setTimeout(() => {
            window.location.href =
                "/dashboard";
        }, 700);

    } catch (error) {

        message.className =
            "alert alert-danger";

        message.textContent =
            error.message;
    }
}


/* -------------------------------
   REGISTER
-------------------------------- */

async function registerUser(event) {

    event.preventDefault();

    const message =
        document.getElementById("formMessage");

    const username =
        document.getElementById("username").value;

    const email =
        document.getElementById("email").value;

    const password =
        document.getElementById("password").value;

    try {

        const data = await apiRequest(
            "/auth/register",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    username,
                    email,
                    password
                })
            }
        );

        message.className =
            "alert alert-success";

        message.textContent =
            data.message;

        setTimeout(() => {
            window.location.href =
                "/dashboard";
        }, 700);

    } catch (error) {

        message.className =
            "alert alert-danger";

        message.textContent =
            error.message;
    }
}


/* -------------------------------
   DISPLAY AI RESULT
-------------------------------- */

function displayResult(data) {

    const result =
        document.getElementById("result");

    if (!result) {
        return;
    }

    const output =
        data.result;

    let html = "";

    html += `
        <h2>${escapeHtml(output.title || "AI Recommendations")}</h2>
        <p class="result-summary">
            ${escapeHtml(output.summary || "")}
        </p>
    `;

    if (Array.isArray(output.recommendations)) {

        output.recommendations.forEach(
            (item) => {

                html += `
                    <div class="recommendation">

                        <h3>
                            ${escapeHtml(item.name || "")}
                        </h3>

                        <p>
                            ${escapeHtml(
                                item.description || ""
                            )}
                        </p>

                        ${
                            item.estimated_price
                            ? `
                                <p>
                                    <strong>
                                        Estimated price:
                                    </strong>
                                    ${escapeHtml(
                                        item.estimated_price
                                    )}
                                </p>
                            `
                            : ""
                        }

                        ${
                            item.reason
                            ? `
                                <p>
                                    <strong>
                                        Why:
                                    </strong>
                                    ${escapeHtml(
                                        item.reason
                                    )}
                                </p>
                            `
                            : ""
                        }

                        ${
                            Array.isArray(item.tips)
                            ? `
                                <ul>
                                    ${item.tips.map(
                                        tip =>
                                            `<li>${escapeHtml(
                                                tip
                                            )}</li>`
                                    ).join("")}
                                </ul>
                            `
                            : ""
                        }

                    </div>
                `;
            }
        );
    }

    if (output.budget_note) {

        html += `
            <div class="budget-note">
                <strong>Budget note:</strong>
                ${escapeHtml(output.budget_note)}
            </div>
        `;
    }

    result.innerHTML = html;

    result.classList.remove("hidden");

    result.scrollIntoView({
        behavior: "smooth"
    });
}


/* -------------------------------
   HTML ESCAPE
-------------------------------- */

function escapeHtml(value) {

    const div =
        document.createElement("div");

    div.textContent =
        String(value ?? "");

    return div.innerHTML;
}


/* -------------------------------
   HOME PLANNER
-------------------------------- */

async function generateHome(event) {

    event.preventDefault();

    const button =
        document.getElementById("generateButton");

    const form =
        document.getElementById("homeForm");

    button.disabled = true;

    button.textContent =
        "Generating...";

    const formData =
        new FormData(form);

    const data = {

        room_type:
            formData.get("room_type"),

        room_size:
            formData.get("room_size"),

        budget:
            Number(formData.get("budget")),

        style:
            formData.get("style"),

        colors:
            formData.get("colors"),

        requirements:
            formData.get("requirements")
    };

    try {

        const result =
            await apiRequest(
                "/generate-home",
                {
                    method: "POST",
                    headers: {
                        "Content-Type":
                            "application/json"
                    },
                    body: JSON.stringify(data)
                }
            );

        displayResult(result);

    } catch (error) {

        alert(error.message);

    } finally {

        button.disabled = false;

        button.textContent =
            "Generate AI Plan";
    }
}


/* -------------------------------
   PARTY PLANNER
-------------------------------- */

async function generateParty(event) {

    event.preventDefault();

    const button =
        document.getElementById("generateButton");

    const form =
        document.getElementById("partyForm");

    button.disabled = true;

    button.textContent =
        "Generating...";

    const formData =
        new FormData(form);

    const data = {

        event_type:
            formData.get("event_type"),

        guests:
            Number(formData.get("guests")),

        budget:
            Number(formData.get("budget")),

        venue:
            formData.get("venue"),

        theme:
            formData.get("theme"),

        food_preference:
            formData.get("food_preference"),

        requirements:
            formData.get("requirements")
    };

    try {

        const result =
            await apiRequest(
                "/generate-party",
                {
                    method: "POST",
                    headers: {
                        "Content-Type":
                            "application/json"
                    },
                    body: JSON.stringify(data)
                }
            );

        displayResult(result);

    } catch (error) {

        alert(error.message);

    } finally {

        button.disabled = false;

        button.textContent =
            "Generate AI Plan";
    }
}


/* -------------------------------
   JEWELRY PLANNER
-------------------------------- */

async function generateJewelry(event) {

    event.preventDefault();

    const button =
        document.getElementById("generateButton");

    const form =
        document.getElementById("jewelryForm");

    button.disabled = true;

    button.textContent =
        "Generating...";

    const formData =
        new FormData(form);

    try {

        const response =
            await fetch(
                "/generate-jewelry",
                {
                    method: "POST",
                    credentials: "include",
                    body: formData
                }
            );

        const data =
            await response.json();

        if (!response.ok) {
            throw new Error(
                data.detail ||
                "Unable to generate recommendation."
            );
        }

        displayResult(data);

    } catch (error) {

        alert(error.message);

    } finally {

        button.disabled = false;

        button.textContent =
            "Generate AI Plan";
    }
}


/* -------------------------------
   HISTORY
-------------------------------- */

async function loadHistory() {

    const container =
        document.getElementById(
            "historyContainer"
        );

    if (!container) {
        return;
    }

    try {

        const data =
            await apiRequest(
                "/api/history"
            );

        const items =
            data.recommendations || [];

        if (items.length === 0) {

            container.innerHTML = `
                <div class="card">
                    <h3>No recommendations yet</h3>
                    <p>
                        Use one of the AI planners
                        to create your first plan.
                    </p>
                </div>
            `;

            return;
        }

        let html = "";

        items.forEach(item => {

            const title =
                item.result_data?.title ||
                "Recommendation";

            html += `
                <div class="card"
                     style="margin-bottom: 18px;">

                    <h3>
                        ${escapeHtml(title)}
                    </h3>

                    <p>
                        <strong>Planner:</strong>
                        ${escapeHtml(
                            item.planner_type
                        )}
                    </p>

                    <p>
                        <strong>Date:</strong>
                        ${escapeHtml(
                            item.created_at
                        )}
                    </p>

                    <a
                        class="btn btn-secondary"
                        href="/history?id=${item.id}">
                        View
                    </a>

                </div>
            `;
        });

        container.innerHTML = html;

    } catch (error) {

        container.innerHTML = `
            <div class="alert alert-danger">
                ${escapeHtml(error.message)}
            </div>
        `;
    }
}


/* -------------------------------
   DASHBOARD
-------------------------------- */

async function loadDashboard() {

    const username =
        document.getElementById(
            "dashboardUsername"
        );

    const count =
        document.getElementById(
            "recommendationCount"
        );

    if (!username && !count) {
        return;
    }

    try {

        const session =
            await apiRequest(
                "/auth/session-data"
            );

        if (username) {
            username.textContent =
                session.user.username;
        }

        const history =
            await apiRequest(
                "/api/history"
            );

        if (count) {

            count.textContent =
                history.recommendations.length;
        }

    } catch (error) {

        console.error(error);
    }
}


/* -------------------------------
   INIT
-------------------------------- */

document.addEventListener(
    "DOMContentLoaded",
    () => {

        loadSession();

        loadHistory();

        loadDashboard();

        const loginForm =
            document.getElementById(
                "loginForm"
            );

        if (loginForm) {
            loginForm.addEventListener(
                "submit",
                loginUser
            );
        }

        const registerForm =
            document.getElementById(
                "registerForm"
            );

        if (registerForm) {
            registerForm.addEventListener(
                "submit",
                registerUser
            );
        }

        const homeForm =
            document.getElementById(
                "homeForm"
            );

        if (homeForm) {
            homeForm.addEventListener(
                "submit",
                generateHome
            );
        }

        const partyForm =
            document.getElementById(
                "partyForm"
            );

        if (partyForm) {
            partyForm.addEventListener(
                "submit",
                generateParty
            );
        }

        const jewelryForm =
            document.getElementById(
                "jewelryForm"
            );

        if (jewelryForm) {
            jewelryForm.addEventListener(
                "submit",
                generateJewelry
            );
        }

        const logoutForm =
            document.getElementById(
                "logoutForm"
            );

        if (logoutForm) {
            logoutForm.addEventListener(
                "submit",
                logout
            );
        }
    }
);