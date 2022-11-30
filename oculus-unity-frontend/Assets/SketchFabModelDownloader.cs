using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using System.IO;
public class SketchFabModelDownloader : MonoBehaviour
{

    string model_url = "https://sketchfab-prod-media.s3.amazonaws.com/archives/5322e7ba8e1848268152e6f82187861d/glb/6cf2bbe7343b4e0d923b353e8df2737e/jupitar.glb?AWSAccessKeyId=ASIAZ4EAQ242MECCSMGO&Signature=r9LUc%2BF6U76lX3zwTLYSPR8oxMk%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEEcaCWV1LXdlc3QtMSJGMEQCIEZY4C0i60FjjLT3V2AJ9sKq6UviOoi386UBxh%2FB0Ou8AiANQdRNR90IUv41Sn3eSNLltE0J0BYi%2BHRSfRp%2B0%2Fa9xirMBAhgEAAaDDY3ODg3NDM3MTg5MiIMvJc2d%2FHoGj9d68CSKqkEevPWxXkG%2Fek7CjAaRzelsNYr6u7V2aoPWnnVZqwk%2Bt13S9XrPDZoyc4F%2Fs8zr9DqEebCBHa5STDrPp6E83%2BxwFB4v9XqWgch%2Bis7UkCGx%2Fkn%2F3Jr%2BnhaH9eSrFlBtuls85873kS6uC2d95Lyf%2BFJAx63KLrpinTwygXLiLpPgPvIskMXbdPNi4Pan%2By5zaXq9DTZ2S4fpOw0UtSzG74gUY9jACu0IbfekzJjtsgBa1Zx%2Fz7MPUZH17nhDERtHTRWbjCv84HMtTVV6ijVSq8QJYAkrWc4SuQ7Htd%2B144762lETsPI4vs%2FRTrTsVVLt9G5sCnWY3lWitYY6tR%2FOHDG9OEkAFUBr%2ByNr7ZuZ6ZaWWSUQm%2FmHMNy1cqNB0RqhlQsZBr4XCRs%2FUjYTXfNOxwt2Ot8xepdqJEwKD6jy9RHqhu6H16P%2B7bbeQvDaOikvxQTQPpXKBXhYpZxvB9KyN0ijcJDg47WlxjHPlTMK2Ze366GWm7iRhx5Zq3n2uJja7I2pkNlXTMJ7yPrBg5e1Awgyct%2BQmqi00EOdULQjIEMnLIah2E4UElZndZLSETOrw6%2FnTeXuF%2Fv89Z9zpGZ1SyttGyLeKJkAZZerzXOS4zJVJUfPAltjiFzJ7nMUUoFgDW2pe8iwQuSHx6d%2BfwmTcMBGZxjpwm3CFhdte4onqHAiu4aX%2BrXaugM%2FtyN14ERSv2paIu4c7pSmG4gcrvsmdZpGRY9ytnWIimv5zCtu5icBjqqAd6rWM47ZGZgT8tog3dVxPDOBskIMx3d9MjcFtuXbktQjnZarG8cVGqSMxoqJzXxeG4CI4ZxHjJSCTIGuafPMRiqxYXdhLNCu8G1EPwZo4uPlM0rft%2FNRtmxh87ISJFmhCRBRltvz%2BkQh9EFj710CGr08scYDdPZWY9dTN%2FOdqWwZ0%2Fp2uvpugaBqo%2FMk%2Fd3LCgQCHo6TLG2WxwQCLB19IDdrV%2B5h5T0jqGi&Expires=1669736284";
    // Start is called before the first frame update
    void Start()
    {
        StartCoroutine(ModelDownloader(model_url, "jupiter"));
        Debug.Log("Sketchfab shit");
    }

    // Update is called once per frame
    void Update()
    {

    }

    // IEnumerator GetModelDownloadDetails(string model_uid)
    // {
    //     UnityWebRequest www = new UnityWebRequest(" https://api.sketchfab.com/v3/models/" + model_uid + "/download");
    //     www.SetRequestHeader("Authorization", "Bearer hZ7DJc4mIAqFCVGs5fyAXIyRqugd4I");
    //     yield return www.SendWebRequest();

    //     if (www.result != UnityWebRequest.Result.Success)
    //     {
    //         Debug.Log(www.error);
    //     }
    //     else
    //     {
    //         // Show results as text
    //         Debug.Log(www.downloadHandler.text);

    //         // Or retrieve results as binary data
    //         //byte[] results = www.downloadHandler.data;
    //     }
    // }

    IEnumerator ModelDownloader(string model_url, string model_name)
    {

        var uwr = new UnityWebRequest(model_url, UnityWebRequest.kHttpVerbGET);
        string path = Path.Combine(Application.persistentDataPath, model_name + ".glb");
        uwr.downloadHandler = new DownloadHandlerFile(path);
        yield return uwr.SendWebRequest();
        if (uwr.result != UnityWebRequest.Result.Success)
            Debug.LogError(uwr.error);
        else
            Debug.Log("File successfully downloaded and saved to " + path);


    }
}
