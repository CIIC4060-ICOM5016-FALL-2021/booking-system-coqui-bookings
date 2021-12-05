import React, {Component, useState} from 'react';
import {Calendar, dateFormat, momentLocalizer, Views} from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import {Button, Card, Container, Form, Grid, Modal, Segment} from "semantic-ui-react";
import axios from "axios";

moment.locale("en-GB");
const localizer = momentLocalizer(moment);


function Schedule() {
    const evs = []
    const [dates, setDates] = useState([{
        'title': 'Selection',
        'allDay': false,
        'start': new Date(moment.now()),
        'end': new Date(moment.now())
    }]);
    const data = {
        user_id: localStorage.getItem("user_id")
    }
        axios.get('https://coqui-bookings-database.herokuapp.com/coqui-bookings/User/unavailable-time-users/' + data.user_id)
            .then(function (response) {
                console.log(response.data);
                let appointments = response.data;
                for (let i = 0; i < appointments.length; i++) {
                    evs.push({
                        'title': "Unavailable",
                        'allDay': false,
                        'start':new Date(appointments[i].unavailable_time_user_start),
                        'end': new Date(appointments[i].unavailable_time_user_finish)
                    })

                    // TODO DO ANOTHER AXIOS TO VERIFY IF BOOKING OR MARKED BY USER
                }
            }).catch(
                err => {
                    console.log("Error:" + err)
                })

    //const [open, setOpen] = useState(false);
    const localizer = momentLocalizer(moment)

    return <Container style={{ height: 800 }}><Calendar
        localizer={localizer}
        startAccessor="start"
        events={evs}
        endAccessor="end"
        views={["month", "day"]}
        defaultDate={Date.now()}
    >

    </Calendar>
    </Container>

        )
    }
}
export default Schedule;

    // const [open, setOpen] = useState(false);
    // const localizer = momentLocalizer(moment)

//     return (<Container style={{ height: 800 }}><Calendar
//         localizer={localizer}
//         startAccessor="start"
//         events={""}
//         endAccessor="end"
//         views={["month", "day"]}
//         defaultDate={Date.now()}
//     >
//
//     </Calendar>
//         <Button
//             fluid
//             onClick={useShowUserSchedule}
//         >Load Schedule </Button>
//     </Container>
//
// )
//}
//export default Schedule;


// import React, {Component, useState} from 'react';
// import {Calendar, dateFormat, momentLocalizer, Views} from 'react-big-calendar';
// import 'react-big-calendar/lib/css/react-big-calendar.css';
// import moment from 'moment';
// import {Button, Card, Container, Form, Grid, Modal, Segment} from "semantic-ui-react";
// import Axios from "axios";
//
// function Schedule(){
//
//     const [date, set_date] = useState("");
//
//     const data = {
//         date : date,
//         user_id: localStorage.getItem("user_id")
//     }
//     async function getUserSchedule(){
//         const schedule = await Axios.get('https://coqui-bookings-database.herokuapp.com/coqui-bookings/User/unavailable-time-users/' + data.user_id)
//             .then(res => {
//                 console.log(res.data)
//                 return res.data
//
//             }).catch(err => {
//                 return "NOT FOUND ERROR";
//             })
//         return schedule;
//     }
//
//     async function useShowUserSchedule() {
//         let [events, setEvents] = useState([]);
//         const user_schedule = await getUserSchedule();
//         for(const k in user_schedule){
//             events.push(new Event("title", user_schedule[k].unavailable_time_ser_start, user_schedule[k].unavailable_time_user_finish));
//         }
//         return events;
//     }
//
//     // const [events, setEvents] = useState([{
//     //     'title':'Unavailable',
//     //     'allDay': false,
//     //     'start': new Date(moment.now()),
//     //     'end': new Date(moment.now())
//     // }]);
//     const test = useShowUserSchedule();
//     const [open, setOpen] = useState(false);
//     const localizer = momentLocalizer(moment)
//
//     return <Container style={{ height: 800 }}><Calendar
//         localizer={localizer}
//         startAccessor="start"
//         events={""}
//         endAccessor="end"
//         views={["month", "day"]}
//         defaultDate={Date.now()}
//     >
//
//     </Calendar>
//         <Button
//             fluid
//             onClick={useShowUserSchedule}
//         >Load Schedule </Button>
//     </Container>
//
//
// }
// export default Schedule;
