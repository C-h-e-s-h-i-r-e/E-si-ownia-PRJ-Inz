import React, {useEffect, useRef, useState} from "react";
import 'bootstrap/dist/css/bootstrap.min.css';
import axiosInstance from "../../Axios/Axios";
import Photo from "../../../imgs/gymcoin.png";
import {Link} from "react-router-dom";
import useCollapse from "react-collapsed";


function TrainingGroupShowTrainerTrainings() {

    const [trainingGroupAll, setTrainingGroupAll] = useState([]);
    const [trainingGroupTypeAll, setTrainingGroupTypeAll] = useState([]);
    const [userInfo, setUserInfo] = useState("");


    useEffect(() => {

        axiosInstance
            .post(`training/group/all`, {}, {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': localStorage.getItem('token_type') + ' ' + localStorage.getItem('access_token')
                }
            })
            .then((res) => {
                setTrainingGroupAll(res.data)
            });

        axiosInstance
            .post(`training/group/type/all`, {}, {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': localStorage.getItem('token_type') + ' ' + localStorage.getItem('access_token')
                }
            })
            .then((res) => {
                setTrainingGroupTypeAll(res.data)
            });

        axiosInstance
            .post(`users/info/`, {}, {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': localStorage.getItem('token_type') + ' ' + localStorage.getItem('access_token')
                }
            })
            .then((res) => {
                setUserInfo(res.data)
            });

    }, []);

    const {getCollapseProps, getToggleProps, isExpanded} = useCollapse()
    const titleRef = useRef()

    function handleBackClick(){
        titleRef.current.scrollIntoView({ behavior: 'smooth' })
    }


    return (
        <div className="trainingGroupShowTrainerTrainings">
            <div className="container">

                <div className="text-center">
                    <hr></hr>
                    <h1 style={{"fontSize": "5vw"}} className="display-1 font-weight-light mb-4">Twoje Grupy
                        (Trener)</h1>
                    <hr></hr>
                </div>
                <div className="row">
                    {/*<div className="col-md-3 border text-center">*/}
                    {/*    Filtowanie*/}
                    {/*</div>*/}
                    <div className="col-md-12 border text-center inline-block">
                        <div id="offer_container" className="row justify-content-center">
                            <div className="row">
                                {trainingGroupAll.map((training, idx) => {
                                    if (training.owner === userInfo.id) {
                                        return (
                                            <div key={idx} style={{minWidth: '250px'}} className="col-md-4 mb-2 flex">
                                                <div className="h-100 card m-1">
                                                    <img src={Photo} width="100%" height="width"
                                                         className="card-img-top rounded-circle"
                                                         alt="..."/>
                                                    <div className="card-body">
                                                        <div>
                                                            <h5 className="card-title">{training.title}</h5>
                                                            <div className="card-subtitle"
                                                                 style={{overflow: 'auto', height: '100px'}}>
                                                                {trainingGroupTypeAll.map(function (type, id) {
                                                                    for (let i = 0; i < training.type.length; i++) {
                                                                        if (training.type.includes(type.id)) {
                                                                            return (<p className="m-0"
                                                                                       key={id}>{type.type}</p>)
                                                                        }
                                                                    }
                                                                })}
                                                            </div>
                                                            <p className="card-text"> Poziom: {training.difficulty}</p>
                                                            <p className="card-text text-center"> Trener: </p>
                                                            <p className="card-text"> Imie: {userInfo.first_name}</p>
                                                            <p className="card-text"> Naziwsko: {userInfo.last_name}</p>
                                                            <Link className='btn' to={{
                                                                pathname: '/strefa_trenera_treningi',
                                                                state: {
                                                                    groupId: training.id
                                                                }
                                                            }}>Szczegóły Grupy {training.id}</Link>
                                                            <button className="btn btn-lg m-4" onClick={handleBackClick} {...getToggleProps()} >
                                                                {isExpanded ? 'Zamknij Edycję' : 'Edytuj Grupę'}
                                                            </button>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        )
                                    }
                                })}
                            </div>
                        </div>
                    </div>

                </div>
            </div>
            <div className="container"  {...getCollapseProps()}>
                <div className="col-md-12 text-center inline-block" >
                    <div className="text-center">
                        <hr></hr>
                        <h1 style={{"fontSize": "5vw"}} className="display-1 font-weight-light mb-4" ref={titleRef}>Edytuj Grupę</h1>
                        <hr></hr>
                    </div>
                    <div id="offer_container" className="row justify-content-center">
                        <div className="row border mt-4">
                            {trainingGroupAll.map((training, idx) => {
                                if (training.owner === userInfo.id) {
                                    return (
                                        <div className="container mt-4">
                                            <section>
                                                <div className="container">
                                                    {training.difficulty}
                                                    {trainingGroupTypeAll.map(function (type, id) {
                                                        for (let i = 0; i < training.type.length; i++) {
                                                            if (training.type.includes(type.id)) {
                                                                return (<p className="m-0"
                                                                        key={id}>{type.type}</p>)
                                                            }
                                                        }
                                                    })}
                                                    {training.description}
                                                    {training.title}
                                                </div>
                                            </section>
                                        </div>

                                    )
                                }
                            })}
                        </div>
                    </div>
                </div>
            </div>

        </div>
    );
}

export default TrainingGroupShowTrainerTrainings;