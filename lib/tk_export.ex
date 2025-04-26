defmodule TkExport do
  require Logger

  @sleep 500

  def export(user_id, cookie) when is_binary(user_id) and is_binary(cookie) do
    campaign_data(user_id) |> Enum.map(&campaign_export/1)
  end

  def request() do
    Req.new(base_url: "https://www.tavern-keeper.com")
    |> Req.Request.put_header("accept", "application/json")
    |> Req.Request.put_header("cookie", "tavern-keeper=#{System.get_env("TK_COOKIE")}")
    |> Req.Request.put_header("X-CSRF-Token", "something")
    |> Req.Request.put_header("User-Agent", "Mozilla/5.0")
  end

  defp campaign_export(campaign) do
    Logger.info("Exporting Campaign #{campaign["id"]}")
    c =
    %{
      id: campaign["id"],
      system_name: campaign["system_name"],
      name: campaign["name"]
    }
    |> characters_export()
    |> scenes_export()

    path = "#{c.name}.json"
    if File.exists?(path), do: File.rm!(path)
    json = Jason.encode!(c)
    File.write(path, json)
    c
  end

  defp characters_export(campaign) do
    characters =
    campaign_character_data(campaign)
    |> Enum.map(fn x ->
      Process.sleep(@sleep)
      character_export(x["id"])
    end)
    Map.put(campaign, :characters, characters)
  end

  defp character_export(character_id) do
    Logger.info("Exporting Character #{character_id}")
    data = character_data(character_id)
    %{
      id: data["id"],
      name: data["name"],
      concept: data["concept"],
      quote: data["quote"],
      nickname: data["nickname"],
      sheet: data["sheet"]["data"]["character"],
      bio: %{
        background: data["biography"]["background"],
        personality: data["biography"]["personality"],
        appearance: data["biography"]["appearance"]
      }
    }
  end

  defp scenes_export(campaign) do
    scenes =
      campaign_roleplay_data(campaign)
    |> Enum.map(fn x ->
      Logger.info("Exporting Scene - #{x["id"]}")
      Process.sleep(@sleep)
      %{
        name: x["name"],
        messages: scene_messages_export(x["id"])
      }

    end)
    Map.put(campaign, :scenes, scenes)
  end

  defp scene_messages_export(scene_id) do
    roleplay_message_data(scene_id)
    |> Enum.map(fn x ->
      %{
        content: x["content"],
        character: x["character"]["name"],
        roll: x["roll"],
        comments: (if x["comment_count"] == 0, do: [], else: roleplay_message_comments_data(scene_id, x["id"]) |> Enum.map(fn x  -> %{name: x["user"]["name"], content: x["content"]} end) )
      }

    end)
  end

  def campaign_data(user_id) do
    response = request()
    |> Req.get!(url: "/api/v0/users/#{user_id}/campaigns")
    
    Logger.info("Response status: #{response.status}")
    Logger.info("Response body: #{inspect(response.body)}")
    
    case response do
      %{status: 200, body: body} when is_map(body) ->
        Map.get(body, "campaigns", [])
      %{status: 404} ->
        Logger.error("User or campaigns not found. Please check the USER_ID and TK_COOKIE values.")
        []
      _ ->
        Logger.error("Unexpected response format: #{inspect(response)}")
        []
    end
  end
  def campaign_character_data(campaign, options \\ []) do
    page = Keyword.get(options, :page, 1)
    data = Keyword.get(options, :data, [])

    request_data =
    request()
    |> Req.get!(url: "/api_v0/campaigns/#{campaign.id}/characters?page=#{page}")
    |> Map.get(:body)

    if request_data["page"] >= request_data["pages"] do
      data ++ request_data["characters"]
    else
      Process.sleep(@sleep)
      campaign_character_data(campaign, [page: page + 1, data: data ++ request_data["characters"]])
    end
  end

  def campaign_roleplay_data(campaign, options \\ []) do
    page = Keyword.get(options, :page, 1)
    data = Keyword.get(options, :data, [])

    request_data =
    request()
    |> Req.get!(url: "/api_v0/campaigns/#{campaign.id}/roleplays?page=#{page}")
    |> Map.get(:body)

    if request_data["page"] >= request_data["pages"] do
      data ++ request_data["roleplays"]
    else
      Process.sleep(@sleep)
      campaign_roleplay_data(campaign, [page: page + 1, data: data ++ request_data["roleplays"]])
    end
  end
  def roleplay_message_data(roleplay_id, options \\ []) do
    page = Keyword.get(options, :page, 1)
    data = Keyword.get(options, :data, [])

    request_data =
    request()
    |> Req.get!(url: "/api_v0/roleplays/#{roleplay_id}/messages?page=#{page}")
    |> Map.get(:body)

    if request_data["page"] >= request_data["pages"] do
      data ++ request_data["messages"]
    else
      Process.sleep(@sleep)
      roleplay_message_data(roleplay_id, [page: page + 1, data: data ++ request_data["messages"]])
    end
  end
  def roleplay_message_comments_data(roleplay_id, message_id, options \\ []) do
    page = Keyword.get(options, :page, 1)
    data = Keyword.get(options, :data, [])

    request_data =
    request()
    |> Req.get!(url: "/api_v0/roleplays/#{roleplay_id}/messages/#{message_id}/comments?page=#{page}")
    |> Map.get(:body)

    if request_data["page"] >= request_data["pages"] do
      data ++ request_data["comments"]
    else
      Process.sleep(@sleep)
      roleplay_message_comments_data(roleplay_id, [page: page + 1, data: data ++ request_data["comments"]])
    end
  end


  def character_data(character_id) do
    request()
    |> Req.get!(url: "/api_v0/characters/#{character_id}")
    |> Map.get(:body)
  end

end
