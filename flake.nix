{
  description = "Python development environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = {
    self,
    nixpkgs,
    flake-utils,
    ...
  }:
    flake-utils.lib.eachDefaultSystem (
      system: let
        pkgs = nixpkgs.legacyPackages.${system};
      in {
        devShells.default = pkgs.mkShell {
          packages = with pkgs; [
            yapf
            pyright
          ];

          buildInputs = with pkgs; [
            python313
            python313Packages.pip
            python313Packages.redis
            python313Packages.httpx
            python313Packages.flask
            python313Packages.requests
            python313Packages.fastapi-cli
            python313Packages.functions-framework
          ];

          shellHook = ''
            echo "Python ${pkgs.python314.version} environment"
            python --version
            pip --version
          '';
        };
      }
    );
}
