
module KoffieFrontendChallenge
using Dash

const resources_path = realpath(joinpath( @__DIR__, "..", "deps"))
const version = "0.0.1"

include("jl/''_tablecomponent.jl")

function __init__()
    DashBase.register_package(
        DashBase.ResourcePkg(
            "koffie_frontend_challenge",
            resources_path,
            version = version,
            [
                DashBase.Resource(
    relative_package_path = "koffie_frontend_challenge.min.js",
    external_url = nothing,
    dynamic = nothing,
    async = nothing,
    type = :js
),
DashBase.Resource(
    relative_package_path = "koffie_frontend_challenge.min.js.map",
    external_url = nothing,
    dynamic = true,
    async = nothing,
    type = :js
)
            ]
        )

    )
end
end
