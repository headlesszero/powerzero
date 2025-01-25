
import os
import configparser


class PZConfig:

    deploy_stages  = ["initialize", "develop", "validate", "finalize"]
    configurations = ["dev", "prod", "learn"]

    @staticmethod
    def add_arguments(parser):
        parser.add_argument(
            "-s", "--stage",
            choices  = PZConfig.deploy_stages,
            required = True,
            help     = "Stage of deployment (i.e. start with initialize, end with finalize)"
        )

        parser.add_argument(
            "-c", "--configuration",
            choices  = PZConfig.configurations,
            required = True,
            help     = "Environment configuration (i.e. what's configured and enabled)"
        )


    @staticmethod
    def get_stage(args) -> str:
        stage = args.stage.lower().strip()

        if stage not in PZConfig.deploy_stages:
            print(f"Error: Unknown stage '{stage}'.  Available stages: ({', '.join(PZConfig.deploy_stages)}).")
            sys.exit(1)

        return stage


    @staticmethod
    def get_configuration(args) -> str:
        config = args.configuration.lower().strip()

        if config not in PZConfig.configurations:
            print(f"Error: Unknown environment '{configuration}'.  Available stages: ({', '.join(PZConfig.configurations)}).")
            sys.exit(1)

        return config


    @staticmethod
    def get_config_file_path(args):
        return os.path.abspath(
            os.path.join(
                os.path.dirname(
                    os.path.abspath(__file__)), "../../config", f"bootstrap_{PZConfig.get_stage(args)}.ini")
        )

    @staticmethod
    def load_config_accessor(args):
        config = configparser.ConfigParser()
        config.read(PZConfig.get_config_file_path(args))
        return config


    @staticmethod
    def print_config_selection(args, task:str):
        from hz_bootstrap import LogColor

        # Use 'cls' for Windows and 'clear' for Unix-like systems
        os.system('cls' if os.name == 'nt' else 'clear')

        stage  = PZConfig.get_stage(args)
        config = PZConfig.get_configuration(args)

        stage_list = f"{LogColor.DARK_GRAY.value}[{'] ['.join(PZConfig.deploy_stages)}]{LogColor.RESET.value}"
        stage_list = stage_list.replace(f"[{stage}]", f"{LogColor.BOLD.value}{LogColor.MAGENTA.value}[{stage.upper()}]{LogColor.RESET.value}{LogColor.DARK_GRAY.value}")

        config_list = f"{LogColor.DARK_GRAY.value}[{'] ['.join(PZConfig.configurations)}]{LogColor.RESET.value}"
        config_list = config_list.replace(f"[{config}]", f"{LogColor.BOLD.value}{LogColor.MAGENTA.value}[{config.upper()}]{LogColor.RESET.value}{LogColor.DARK_GRAY.value}")


        print(f"{LogColor.UNDERLINE.value}{LogColor.YELLOW.value}{task}:{LogColor.RESET.value}")
        print(f"{LogColor.BLUE.value}Deploy Stage:  {stage_list}")
        print(f"{LogColor.BLUE.value}Configuration: {config_list}")
        print("")






