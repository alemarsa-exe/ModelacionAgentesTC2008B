// TC2008B. Sistemas Multiagentes y Gráficas Computacionales
// C# client to interact with Python. Based on the code provided by Sergio Ruiz.
// Octavio Navarro. November 2022

using System;
using System.Collections;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;
using UnityEngine.Networking;

[Serializable]
public class BoidData
{
    public string carId, lightId;
    public float x, y, z;
    public int typeCar;

    public BoidData(string carId, float x, float y, float z, int typeCar)
    {
        this.carId = carId;
        this.x = x;
        this.y = y;
        this.z = z;
        this.typeCar = typeCar;
    }
}

[Serializable]
public class BoidsData
{
    public List<BoidData> positions;

    public BoidsData() => this.positions = new List<BoidData>();
}

[Serializable]
public class TrafficData
{
    public string lightId;
    public string state;

    public TrafficData(string lightId, string state)
    {
        this.lightId = lightId;
        this.state = state;
    }
}

[Serializable]
public class TrafficsData
{
    public List<TrafficData> trafficLights;
    public TrafficsData() => this.trafficLights = new List<TrafficData>();
}

public class AgentControllerUpdate : MonoBehaviour
{
    private string uri = "http://localhost:8585";
    // private string uri = "http://multiagentesintegradora.us-south.cf.appdomain.cloud/";

    BoidsData boidsData;
    TrafficsData trafficsData;

    Dictionary<string, Vector3> boidsPrevPositions, boidsCurrPositions;
    public GameObject[] agentPrefab;
    Dictionary<string, GameObject> agents;
    public float timeToUpdate = 20.0f;
    private float timer, dt;
    private bool started = false, updated = false;

    void Start()
    {
        boidsData = new BoidsData();
        trafficsData = new TrafficsData();

        agents = new Dictionary<string, GameObject>();

        boidsPrevPositions = new Dictionary<string, Vector3>();
        boidsCurrPositions = new Dictionary<string, Vector3>();

        timer = timeToUpdate;

        StartCoroutine(StartSimulation());
    }

    IEnumerator StartSimulation()
    {
        using (UnityWebRequest webRequest = UnityWebRequest.Get($"{uri}/init"))
        {
            Debug.Log("Starting...");
            yield return webRequest.SendWebRequest();

            if (webRequest.result != UnityWebRequest.Result.Success)
            {
                Debug.Log(webRequest.error);
            }
            else
            {
                Debug.Log($" Starting simulation with: {webRequest.downloadHandler.text}");

                StartCoroutine(GetBoidsData());
                StartCoroutine(GetTrafficData());
            }
        }
    }

    IEnumerator GetBoidsData()
    {
        using (UnityWebRequest webRequest = UnityWebRequest.Get($"{uri}/init"))
        {
            yield return webRequest.SendWebRequest();

            if (webRequest.result != UnityWebRequest.Result.Success)
                Debug.Log(webRequest.error);
            else
            {
                Debug.Log(webRequest.downloadHandler.text);
                boidsData = JsonUtility.FromJson<BoidsData>(webRequest.downloadHandler.text);

                foreach (BoidData boid in boidsData.positions)
                {
                    Vector3 newBoidPosition = new Vector3(boid.x, boid.y, boid.z);
                    GameObject newAgent;

                    if (boid.typeCar == 1)
                    {
                        newAgent = agentPrefab[0];
                        newAgent.transform.Rotate(0, 180, 0);
                        //newAgent = GameObject.Find("Ferrari");
                    }
                    // ESTOS SON BUENOS
                    else if (boid.typeCar == 2)
                    {
                        newAgent = agentPrefab[1];
                        //newAgent = GameObject.Find("Camion");
                    }
                    else if (boid.typeCar == 3)
                    {
                        newAgent = agentPrefab[2];
                        //newAgent = GameObject.Find("RB18");
                    }
                    else
                    {
                        newAgent = agentPrefab[3];
                        //newAgent = GameObject.Find("Helados");
                    }



                    if (!started)
                    {
                        boidsPrevPositions[boid.carId] = newBoidPosition;
                        agents[boid.carId] = Instantiate(newAgent, newBoidPosition, Quaternion.identity);
                    }
                    else
                    {
                        Vector3 currentPosition = new Vector3();
                        if (boidsCurrPositions.TryGetValue(boid.carId, out currentPosition))
                            boidsPrevPositions[boid.carId] = currentPosition;
                        boidsCurrPositions[boid.carId] = newBoidPosition;
                    }
                }

                updated = true;
                if (!started) started = true;
            }
        }
    }

    IEnumerator GetTrafficData()
    {
        using (UnityWebRequest webRequest = UnityWebRequest.Get($"{uri}/init"))
        {
            yield return webRequest.SendWebRequest();

            if (webRequest.result != UnityWebRequest.Result.Success)
                Debug.Log(webRequest.error);
            else
            {
                Debug.Log(webRequest.downloadHandler.text);
                trafficsData = JsonUtility.FromJson<TrafficsData>(webRequest.downloadHandler.text);
                Light currectLight;
                foreach (TrafficData traffic in trafficsData.trafficLights)
                {
                    Debug.Log(traffic.lightId);
                    Debug.Log("ENTRE EN SEMAFORS");
                    if (traffic.lightId == "36")
                    {
                        Light light1 = GameObject.Find("Luces1").GetComponent<Light>();
                        if (traffic.state == "Green")
                        {
                            light1.color = Color.green;
                        }
                        if (traffic.state == "Red")
                        {
                            light1.color = Color.red;
                        }
                    }
                    if (traffic.lightId == "38")
                    {
                        Light light1 = GameObject.Find("Luces3").GetComponent<Light>();
                        if (traffic.state == "Green")
                        {
                            light1.color = Color.green;
                        }
                        if (traffic.state == "Red")
                        {
                            light1.color = Color.red;
                        }
                    }
                    if (traffic.lightId == "40")
                    {
                        Light light1 = GameObject.Find("Luces5").GetComponent<Light>();
                        if (traffic.state == "Green")
                        {
                            light1.color = Color.green;
                        }
                        if (traffic.state == "Red")
                        {
                            light1.color = Color.red;
                        }
                    }
                    if (traffic.lightId == "43")
                    {
                        Light light1 = GameObject.Find("Luces8").GetComponent<Light>();
                        if (traffic.state == "Green")
                        {
                            light1.color = Color.green;
                        }
                        if (traffic.state == "Red")
                        {
                            light1.color = Color.red;
                        }
                    }
                }

                updated = true;
            }
        }
    }

    void Update()
    {
        if (updated)
        {
            timer -= Time.deltaTime;
            dt = 1.0f - (timer / timeToUpdate);
        }

        if (timer < 0)
        {
            timer = timeToUpdate;
            updated = false;
            StartCoroutine(GetBoidsData());
            StartCoroutine(GetTrafficData());

        }

        foreach (var boid in boidsCurrPositions)
        {
            Vector3 currentPosition = boid.Value;
            Vector3 previousPosition = boidsPrevPositions[boid.Key];

            Vector3 interpolated = Vector3.Lerp(previousPosition, currentPosition, dt);
            Vector3 direction = currentPosition - previousPosition;

            agents[boid.Key].transform.localPosition = interpolated;
            agents[boid.Key].transform.rotation = Quaternion.LookRotation(direction);
        }
    }
}
