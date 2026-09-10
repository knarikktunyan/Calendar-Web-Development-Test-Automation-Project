const VALID_USERNAME = "admin";
const VALID_PASSWORD = "admin123";

let currentDate = new Date();

let events = JSON.parse(
    localStorage.getItem("calendarEvents") || "[]"
);



const loginPage = document.getElementById("login-page");
const calendarPage = document.getElementById("calendar-page");

const loginForm = document.getElementById("login-form");
const usernameInput = document.getElementById("username");
const passwordInput = document.getElementById("password");
const loginError = document.getElementById("login-error");

const logoutButton = document.getElementById("logout-button");

const previousMonthButton =
    document.getElementById("previous-month");

const nextMonthButton =
    document.getElementById("next-month");

const currentMonthElement =
    document.getElementById("current-month");

const calendarDays =
    document.getElementById("calendar-days");

const addEventButton =
    document.getElementById("add-event-button");

const eventModal =
    document.getElementById("event-modal");

const eventForm =
    document.getElementById("event-form");

const eventIdInput =
    document.getElementById("event-id");

const eventTitleInput =
    document.getElementById("event-title");

const eventDateInput =
    document.getElementById("event-date");

const titleError =
    document.getElementById("title-error");

const dateError =
    document.getElementById("date-error");

const modalTitle =
    document.getElementById("modal-title");

const closeModalButton =
    document.getElementById("close-modal");

const cancelEventButton =
    document.getElementById("cancel-event");




loginForm.addEventListener("submit", function (event) {

    event.preventDefault();

    const username = usernameInput.value.trim();
    const password = passwordInput.value;

    loginError.classList.add("hidden");

    if (!username || !password) {

        loginError.textContent =
            "Username and password are required.";

        loginError.classList.remove("hidden");

        return;
    }

    if (
        username !== VALID_USERNAME ||
        password !== VALID_PASSWORD
    ) {

        loginError.textContent =
            "Incorrect username or password.";

        loginError.classList.remove("hidden");

        return;
    }

    localStorage.setItem("loggedIn", "true");

    loginPage.classList.add("hidden");
    calendarPage.classList.remove("hidden");

    renderCalendar();
});



logoutButton.addEventListener("click", function () {

    localStorage.removeItem("loggedIn");

    calendarPage.classList.add("hidden");
    loginPage.classList.remove("hidden");

    usernameInput.value = "";
    passwordInput.value = "";
    loginError.classList.add("hidden");
});


previousMonthButton.addEventListener("click", function () {

    currentDate.setMonth(currentDate.getMonth() - 1);

    renderCalendar();
});


nextMonthButton.addEventListener("click", function () {

    currentDate.setMonth(currentDate.getMonth() + 1);

    renderCalendar();
});



addEventButton.addEventListener("click", function () {

    openAddEventModal();
});



closeModalButton.addEventListener(
    "click",
    closeEventModal
);

cancelEventButton.addEventListener(
    "click",
    closeEventModal
);


function openAddEventModal() {

    modalTitle.textContent = "Add Event";

    eventIdInput.value = "";
    eventTitleInput.value = "";
    eventDateInput.value = "";

    titleError.classList.add("hidden");
    dateError.classList.add("hidden");

    eventModal.classList.remove("hidden");
}


function openEditEventModal(eventObject) {

    modalTitle.textContent = "Edit Event";

    eventIdInput.value = eventObject.id;
    eventTitleInput.value = eventObject.title;
    eventDateInput.value = eventObject.date;

    titleError.classList.add("hidden");
    dateError.classList.add("hidden");

    eventModal.classList.remove("hidden");
}


function closeEventModal() {

    eventModal.classList.add("hidden");

    eventForm.reset();

    titleError.classList.add("hidden");
    dateError.classList.add("hidden");
}




eventForm.addEventListener("submit", function (event) {

    event.preventDefault();

    const title = eventTitleInput.value.trim();
    const date = eventDateInput.value;

    let valid = true;

    titleError.classList.add("hidden");
    dateError.classList.add("hidden");


    if (!title) {

        titleError.classList.remove("hidden");

        valid = false;
    }


    if (!date) {

        dateError.classList.remove("hidden");

        valid = false;
    }


    if (!valid) {
        return;
    }


    const existingId = eventIdInput.value;


    if (existingId) {

        const eventIndex = events.findIndex(
            item => item.id === existingId
        );

        if (eventIndex !== -1) {

            events[eventIndex].title = title;
            events[eventIndex].date = date;
        }

    } else {

        const newEvent = {

            id: Date.now().toString(),

            title: title,

            date: date
        };

        events.push(newEvent);
    }


    saveEvents();

    closeEventModal();

    renderCalendar();
});


function saveEvents() {

    localStorage.setItem(
        "calendarEvents",
        JSON.stringify(events)
    );
}



function deleteEvent(eventId) {

    events = events.filter(
        item => item.id !== eventId
    );

    saveEvents();

    renderCalendar();
}


function renderCalendar() {

    const year = currentDate.getFullYear();

    const month = currentDate.getMonth();

    const monthName = currentDate.toLocaleString(
        "default",
        {
            month: "long"
        }
    );


    currentMonthElement.textContent =
        `${monthName} ${year}`;


    calendarDays.innerHTML = "";


    const firstDay = new Date(
        year,
        month,
        1
    ).getDay();


    const daysInMonth = new Date(
        year,
        month + 1,
        0
    ).getDate();


    const daysInPreviousMonth = new Date(
        year,
        month,
        0
    ).getDate();


    for (let i = firstDay - 1; i >= 0; i--) {

        const dayNumber =
            daysInPreviousMonth - i;

        createDayElement(
            dayNumber,
            true,
            null
        );
    }



    for (
        let day = 1;
        day <= daysInMonth;
        day++
    ) {

        const dateString =
            formatDate(year, month + 1, day);

        createDayElement(
            day,
            false,
            dateString
        );
    }


    const totalCells =
        calendarDays.children.length;

    const remaining =
        42 - totalCells;


    for (
        let day = 1;
        day <= remaining;
        day++
    ) {

        createDayElement(
            day,
            true,
            null
        );
    }
}



function createDayElement(
    dayNumber,
    isOtherMonth,
    dateString
) {

    const dayElement =
        document.createElement("div");

    dayElement.className =
        "calendar-day";


    if (isOtherMonth) {

        dayElement.classList.add(
            "other-month"
        );
    }


    const numberElement =
        document.createElement("div");

    numberElement.className =
        "day-number";

    numberElement.textContent =
        dayNumber;


    dayElement.appendChild(
        numberElement
    );


    if (dateString) {

        const today =
            new Date();


        const todayString =
            formatDate(
                today.getFullYear(),
                today.getMonth() + 1,
                today.getDate()
            );


        if (dateString === todayString) {

            dayElement.classList.add(
                "today"
            );
        }


        const dayEvents =
            events.filter(
                item => item.date === dateString
            );


        dayEvents.forEach(
            eventObject => {

                const eventElement =
                    document.createElement("div");

                eventElement.className =
                    "event";


                const title =
                    document.createElement("span");

                title.className =
                    "event-title";

                title.textContent =
                    eventObject.title;


                const buttons =
                    document.createElement("div");

                buttons.className =
                    "event-buttons";


                const editButton =
                    document.createElement("button");

                editButton.textContent =
                    "Edit";

                editButton.type =
                    "button";

                editButton.setAttribute(
                    "data-testid",
                    `edit-event-${eventObject.id}`
                );


                editButton.addEventListener(
                    "click",
                    function () {

                        openEditEventModal(
                            eventObject
                        );
                    }
                );


                const deleteButton =
                    document.createElement("button");

                deleteButton.textContent =
                    "Delete";

                deleteButton.type =
                    "button";

                deleteButton.setAttribute(
                    "data-testid",
                    `delete-event-${eventObject.id}`
                );


                deleteButton.addEventListener(
                    "click",
                    function () {

                        deleteEvent(
                            eventObject.id
                        );
                    }
                );


                buttons.appendChild(
                    editButton
                );

                buttons.appendChild(
                    deleteButton
                );


                eventElement.appendChild(
                    title
                );

                eventElement.appendChild(
                    buttons
                );


                dayElement.appendChild(
                    eventElement
                );
            }
        );
    }


    calendarDays.appendChild(
        dayElement
    );
}




function formatDate(
    year,
    month,
    day
) {

    return `${year}-${String(month).padStart(2, "0")}-${String(day).padStart(2, "0")}`;
}



function initializeApp() {

    const loggedIn =
        localStorage.getItem("loggedIn");


    if (loggedIn === "true") {

        loginPage.classList.add("hidden");

        calendarPage.classList.remove(
            "hidden"
        );

        renderCalendar();

    } else {

        loginPage.classList.remove(
            "hidden"
        );

        calendarPage.classList.add(
            "hidden"
        );
    }
}


initializeApp();
