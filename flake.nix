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
        pkgs = import nixpkgs {
          inherit system;
          config = {
            allowUnfree = true;
          };
        };
      in {
        devShells.default = pkgs.mkShell {
          packages = with pkgs; [
            yapf
            pyright
          ];

          buildInputs = with pkgs; [
            python313
            terraform
            terraform-ls
            google-cloud-sdk
            python313Packages.pip
            python313Packages.httpx
            python313Packages.flask
            python313Packages.functions-framework
          ];

          shellHook = ''
            echo "Python ${pkgs.python313.version} environment"
          '';
        };
      }
    );
}
