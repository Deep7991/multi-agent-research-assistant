async function generateReport(){

    const topic=document.getElementById("topic").value;

    if(topic===""){

        alert("Enter a topic");

        return;
    }

    document.getElementById("status").innerHTML="Researching...";

    document.getElementById("output").innerHTML="";

    const response=await fetch("/generate",{

        method:"POST",

        headers:{

            "Content-Type":"application/json"
        },

        body:JSON.stringify({

            topic:topic
        })
    });

    const data=await response.json();

    document.getElementById("status").innerHTML=
`
✅ Completed

Score : ${data.score}

Iterations : ${data.iterations}
`;

    document.getElementById("output").innerHTML=data.report;
}